#!/usr/bin/env python3
"""Geometry Engine prototype: exact finite qubit witness and repair audit.

Models an ideal single-qubit state by a Bloch vector (x,y,z) and a
measurement by the probability of its +1 outcome along X, Y, or Z.

Given a retained measurement signature pi and a required target signature W,
finds distinct states with pi(s)=pi(t) but W(s)!=W(t). It reports the exact
uniform-population squared-loss floor and the least-cost fixed batch of
additional available basis measurements that repairs the witness for the
supplied finite state set.

Compare every available measurement batch, or set a budget to find the batch
with the smallest remaining loss. Costs and losses use exact rational arithmetic.
The full-repair minimum is reported separately from the budget recommendation.

This is a deterministic ideal-probability audit, NOT a one-shot quantum-state
reconstruction, hardware experiment, or finite-sample statistical guarantee.
Repeated independently prepared specimens would be required to estimate the
probabilities used here.

Usage:
    python geometry_quantum_witness.py
    python geometry_quantum_witness.py --example seven
    python geometry_quantum_witness.py --example seven --compare --budget 1
    python geometry_quantum_witness.py --input experiment.json --json
    python geometry_quantum_witness.py --self-test

Input example:
{
  "states": [
    {"id":"plus", "bloch":[1,0,0]},
    {"id":"mixed", "bloch":[0,0,0]}
  ],
  "retained": ["Z"],
  "target": ["X"],
  "available": {"X":1,"Y":2},
  "budget": 1
}

budget is optional; --budget overrides it. Coordinates, costs, and budgets accept
integers, JSON decimals, or quoted fractions such as "1/3". Decimal JSON values
are parsed exactly. Recommendations minimize loss, then cost, number of added
axes, and alphabetical axis order. The frontier keeps one such representative
for each cost/loss point that no other batch improves without a tradeoff.
"""

import argparse
import itertools
import json
import sys
from dataclasses import dataclass
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

AXES = {"X": 0, "Y": 1, "Z": 2}


@dataclass(frozen=True)
class State:
    label: str
    bloch: tuple


def frac(v, field='value'):
    if isinstance(v, bool):
        raise ValueError(f'{field} must be a finite number or fraction, not a Boolean')
    if not isinstance(v, (str, int, float, Decimal, Fraction)):
        raise ValueError(f'{field} must be a finite number or fraction')
    try:
        return Fraction(str(v))
    except (ValueError, ZeroDivisionError, OverflowError) as exc:
        raise ValueError(f'{field} must be a finite number or fraction') from exc


def nonnegative(v, field):
    value = frac(v, field)
    if value < 0:
        raise ValueError(f'{field} must be nonnegative')
    return value


def load_json(text):
    """Retain exact JSON decimals and reject ambiguous duplicate object keys."""
    def unique_object(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f'Duplicate JSON key: {key!r}')
            result[key] = value
        return result

    def invalid_constant(value):
        raise ValueError(f'Non-finite JSON number: {value}')

    return json.loads(text, parse_float=Decimal, parse_constant=invalid_constant,
                      object_pairs_hook=unique_object)


def read_input(data):
    if not isinstance(data, dict):
        raise ValueError('Top-level input must be a JSON object')
    raw = data.get('states')
    if not isinstance(raw, list) or not raw:
        raise ValueError('states must be a nonempty list')
    states = []
    seen = set()
    for index, s in enumerate(raw):
        if not isinstance(s, dict):
            raise ValueError(f'states[{index}] must be an object')
        label = s.get('id')
        if not isinstance(label, str) or not label.strip() or label in seen:
            raise ValueError('Every state must have a unique nonempty string id')
        seen.add(label)
        values = s.get('bloch')
        if not isinstance(values, list) or len(values) != 3:
            raise ValueError(f'states[{index}].bloch must be an array of three coordinates')
        vector = tuple(frac(v, f'states[{index}].bloch[{j}]')
                       for j, v in enumerate(values))
        if sum(x*x for x in vector) > 1:
            raise ValueError(f'Invalid Bloch state {label}: ||r||² > 1')
        states.append(State(label, vector))
    retained, target = data.get('retained'), data.get('target')
    if not isinstance(retained, list) or not isinstance(target, list) or not target:
        raise ValueError('retained and nonempty target must be arrays of axis labels')
    for axes in (retained, target):
        if any(not isinstance(a, str) or a not in AXES for a in axes) or len(set(axes)) != len(axes):
            raise ValueError('Axes must be unique labels from X, Y, Z')
    available = data.get('available', {})
    if not isinstance(available, dict):
        raise ValueError('available must map axis labels to nonnegative measurement costs')
    costs = {}
    for axis, cost in available.items():
        if axis not in AXES:
            raise ValueError(f'Unknown axis {axis}')
        c = nonnegative(cost, f'available.{axis}')
        if axis not in retained:
            costs[axis] = c
    return states, retained, target, costs


def signature(state, axes):
    return tuple((Fraction(1) + state.bloch[AXES[a]]) / 2 for a in axes)


def groups(states, axes):
    out = {}
    for state in states:
        out.setdefault(signature(state, axes), []).append(state)
    return out


def bad_pairs(states, retained, target):
    pairs = []
    for same_pi in groups(states, retained).values():
        for a, b in itertools.combinations(same_pi, 2):
            if signature(a, target) != signature(b, target):
                pairs.append((a, b))
    return pairs


def native_loss(states, retained, target):
    """Uniform over the supplied states; squared Euclidean target probability loss."""
    N = len(states)
    loss = Fraction(0)
    for group in groups(states, retained).values():
        values = [signature(s, target) for s in group]
        means = [sum(v[j] for v in values) / len(values) for j in range(len(target))]
        loss += sum(sum((v[j] - means[j])**2 for j in range(len(target))) for v in values)
    return loss / N


def repair(states, retained, target, costs):
    pairs = bad_pairs(states, retained, target)
    if not pairs:
        return (), Fraction(0), []
    options = sorted(costs)
    unresolved = [(a.label, b.label) for a, b in pairs
                  if not any(signature(a, [c]) != signature(b, [c]) for c in options)]
    if unresolved:
        return None, None, unresolved
    solution = None
    for k in range(len(options) + 1):
        for subset in itertools.combinations(options, k):
            if all(any(signature(a, [c]) != signature(b, [c]) for c in subset)
                   for a, b in pairs):
                cost = sum((costs[c] for c in subset), Fraction(0))
                candidate = (cost, len(subset), subset)
                if solution is None or candidate < solution:
                    solution = candidate
    return solution[2], solution[0], []


def rational(f):
    return str(f.numerator) if f.denominator == 1 else f'{f.numerator}/{f.denominator}'


def measurement_options(states, retained, target, costs):
    """All at most eight fixed batches, in increasing cost then axis order."""
    options = []
    for count in range(len(costs) + 1):
        for axes in itertools.combinations(sorted(costs), count):
            options.append({
                'axes': axes,
                'cost': sum((costs[a] for a in axes), Fraction(0)),
                'loss': native_loss(states, retained + list(axes), target),
            })
    return sorted(options, key=lambda o: (o['cost'], len(o['axes']), o['axes']))


def option_output(option):
    return {'axes': list(option['axes']), 'cost': rational(option['cost']),
            'native_squared_loss_after': rational(option['loss']),
            'repairs_witness': option['loss'] == 0}


def cost_loss_frontier(options):
    frontier = []
    seen = set()
    for option in options:
        point = (option['cost'], option['loss'])
        if point in seen:
            continue
        seen.add(point)
        dominated = any(other['cost'] <= option['cost'] and
                        other['loss'] <= option['loss'] and
                        (other['cost'], other['loss']) != point
                        for other in options)
        if not dominated:
            frontier.append(option)
    return frontier


def run(data, budget=None):
    states, retained, target, costs = read_input(data)
    if budget is not None:
        budget = nonnegative(budget, 'budget')
    elif 'budget' in data:
        budget = nonnegative(data['budget'], 'budget')
    conflicts = bad_pairs(states, retained, target)
    subset, cost, unresolved = repair(states, retained, target, costs)
    options = measurement_options(states, retained, target, costs)
    best = None if budget is None else min(
        (option for option in options if option['cost'] <= budget),
        key=lambda option: (option['loss'], option['cost'], len(option['axes']), option['axes']))
    output = {
        'model': 'ideal single-qubit Bloch states / exact Born probabilities',
        'states': [s.label for s in states],
        'retained_axes': retained,
        'target_axes': target,
        'fibers': [
            {'pi': [rational(a) for a in key], 'states': [s.label for s in members]}
            for key, members in groups(states, retained).items()
        ],
        'non_descent': bool(conflicts),
        'conflicting_pairs': [
            {'states': [a.label, b.label],
             'pi': [rational(v) for v in signature(a, retained)],
             'W_a': [rational(v) for v in signature(a, target)],
             'W_b': [rational(v) for v in signature(b, target)]}
            for a, b in conflicts
        ],
        'native_squared_loss_before': rational(native_loss(states, retained, target)),
        'min_cost_fixed_batch': None if subset is None else {
            'axes': list(subset), 'cost': rational(cost),
            'native_squared_loss_after': rational(native_loss(states, retained + list(subset), target))
        },
        'unrepairable_pairs_with_available_measurements': unresolved,
        'measurement_options': [option_output(option) for option in options],
        'cost_loss_frontier': [option_output(option) for option in cost_loss_frontier(options)],
        'budget': None if budget is None else rational(budget),
        'best_within_budget': None if best is None else option_output(best),
        'scope': 'Finite supplied states, exact ideal probabilities, uniform weights; '
                 'no one-shot reconstruction or hardware/finite-shot claims.'
    }
    return output


def example(which):
    if which == 'two':
        return {
            'states': [{'id': '|+>', 'bloch': [1,0,0]},
                       {'id': 'I/2', 'bloch': [0,0,0]}],
            'retained': ['Z'], 'target': ['X'], 'available': {'X': 1, 'Y': 2}
        }
    return {
        'states': [
            {'id':'|0>', 'bloch':[0,0,1]}, {'id':'|1>', 'bloch':[0,0,-1]},
            {'id':'|+>', 'bloch':[1,0,0]}, {'id':'|->', 'bloch':[-1,0,0]},
            {'id':'|+i>', 'bloch':[0,1,0]}, {'id':'|-i>', 'bloch':[0,-1,0]},
            {'id':'I/2', 'bloch':[0,0,0]},
        ], 'retained':['Z'], 'target':['X','Y','Z'],
        'available':{'X': 2, 'Y': 1}
    }


def self_test():
    def check(condition, message):
        # Keep tests active even when Python runs with -O.
        if not condition:
            raise AssertionError(message)

    t = run(example('two'))
    check(t['non_descent'] and t['native_squared_loss_before'] == '1/16', 'two-state loss')
    check(t['min_cost_fixed_batch'] == {'axes': ['X'], 'cost': '1', 'native_squared_loss_after': '0'}, 'two-state repair')
    s = run(example('seven'))
    check(s['non_descent'] and s['native_squared_loss_before'] == '1/7', 'seven-state loss')
    check(s['min_cost_fixed_batch'] == {'axes': ['X','Y'], 'cost': '3', 'native_squared_loss_after': '0'}, 'seven-state repair')
    # A physically identical retained signature can hide X or Y coherence.
    no_repair = example('two'); no_repair['available'] = {'Y':1}
    check(run(no_repair)['min_cost_fixed_batch'] is None, 'unavailable repair')
    # Exact retained observations already sufficient for a target.
    resolved = example('two'); resolved['retained'] = ['X']; resolved['available'] = {}
    check(not run(resolved)['non_descent'], 'already resolved')
    # Partial information has value even when full repair is out of budget.
    limited = run(example('seven'), budget='1')
    check(limited['best_within_budget'] == {
        'axes': ['Y'], 'cost': '1', 'native_squared_loss_after': '1/14',
        'repairs_witness': False}, 'partial repair under budget')
    check(run(example('seven'), budget=0)['best_within_budget']['axes'] == [], 'zero budget')
    check(run(example('seven'), budget=3)['best_within_budget']['repairs_witness'], 'full repair under budget')
    free = example('two'); free['available'] = {'X': 0, 'Y': 0}
    check(run(free, budget=0)['best_within_budget']['axes'] == ['X'], 'free measurements and tie break')
    exact = load_json('{"states":[{"id":"a","bloch":[0,0,0]}],'
                      '"retained":[],"target":["X"],'
                      '"available":{"X":0.10000000000000000001}}')
    check(read_input(exact)[3]['X'] == Fraction('0.10000000000000000001'), 'exact JSON decimal')
    check([o['cost'] for o in limited['cost_loss_frontier']] == ['0', '1', '3'], 'cost/loss frontier')
    for invalid in [None, True, -1, '1/0', 'NaN', []]:
        bad = example('two'); bad['budget'] = invalid
        try:
            run(bad)
        except ValueError:
            pass
        else:
            raise AssertionError(f'Accepted invalid budget {invalid!r}')
    for invalid in ['{"a":1,"a":2}', '{"a":NaN}', '{"a":Infinity}']:
        try:
            load_json(invalid)
        except ValueError:
            pass
        else:
            raise AssertionError('Accepted ambiguous or non-finite JSON')
    print('PASS: exact losses, repairs, budgets, frontier, decimals, and invalid inputs')


def print_comparison(output):
    print('\nMEASUREMENT OPTIONS')
    print(f'{"Added axes":<14} {"Cost":>12} {"Remaining loss":>20}  Result')
    frontier_axes = {tuple(option['axes']) for option in output['cost_loss_frontier']}
    for option in output['measurement_options']:
        flags = ['full repair' if option['repairs_witness'] else 'partial information']
        if tuple(option['axes']) in frontier_axes:
            flags.append('frontier')
        if option == output['best_within_budget']:
            flags.append('best within budget')
        print(f'{", ".join(option["axes"]) or "(none)":<14} '
              f'{option["cost"]:>12} {option["native_squared_loss_after"]:>20}  '
              + '; '.join(flags))
    print('Frontier: no batch has both lower/equal cost and lower/equal loss with one strict improvement.')


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--input', type=Path, help='Custom experiment JSON; see docstring for schema')
    ap.add_argument('--example', choices=['two','seven'], default='two')
    ap.add_argument('--json', action='store_true', help='Write machine-readable result')
    ap.add_argument('--budget', help='Maximum added measurement cost; accepts decimals or fractions')
    ap.add_argument('--compare', action='store_true', help='Show every batch, cost, and remaining loss')
    ap.add_argument('--self-test', action='store_true')
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    try:
        data = load_json(args.input.read_text(encoding='utf-8-sig')) if args.input else example(args.example)
        output = run(data, budget=args.budget)
    except (ValueError, OSError) as exc:
        if args.json:
            print(json.dumps({'error': str(exc)}, ensure_ascii=False), file=sys.stderr)
            return 2
        ap.error(str(exc))
    if args.json:
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        print('GEOMETRY ENGINE — QUANTUM WITNESS TEST')
        print('States:', ', '.join(output['states']))
        print('Retained basis:', ', '.join(output['retained_axes']))
        print('Required witness:', ', '.join(output['target_axes']))
        print('Non-descent:', 'YES' if output['non_descent'] else 'NO')
        print('Conflicting state pairs:', len(output['conflicting_pairs']))
        for pair in output['conflicting_pairs'][:5]:
            print('  ', ' vs '.join(pair['states']),
                  'same retained signature', pair['pi'],
                  'different targets', pair['W_a'], pair['W_b'])
        if len(output['conflicting_pairs']) > 5:
            print('  ...', len(output['conflicting_pairs'])-5, 'more pairs (use --json)')
        print('Minimum squared-error floor before repair:', output['native_squared_loss_before'])
        r = output['min_cost_fixed_batch']
        if r is None:
            print('REPAIR: IMPOSSIBLE using offered measurements')
            print('Unrepairable pairs:', output['unrepairable_pairs_with_available_measurements'])
        else:
            print('MINIMUM-COST REPAIR:', ', '.join(r['axes']) or '(no extra measurement needed)')
            print('Declared acquisition cost:', r['cost'])
            print('Minimum squared-error floor after repair:', r['native_squared_loss_after'])
        if output['best_within_budget'] is not None:
            best = output['best_within_budget']
            print('BUDGET:', output['budget'])
            print('BEST WITHIN BUDGET:', ', '.join(best['axes']) or '(no extra measurement)')
            print('Cost:', best['cost'], '| Remaining squared-error floor:', best['native_squared_loss_after'])
            print('Full repair:', 'YES' if best['repairs_witness'] else 'NO')
        if args.compare:
            print_comparison(output)
        print('SCOPE:', output['scope'])
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
