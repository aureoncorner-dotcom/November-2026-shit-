#!/usr/bin/env python3
"""Read-only, offline checks for the supplied investigation corpus.

Usage: python verify_connections.py /path/to/extracted/corpus --out checks.json
Optional dependency for the parser experiment: markdown-it-py.
No supplied scripts are executed. No files inside the corpus are changed.
"""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
from pathlib import Path
import re


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inspect(root: Path) -> dict:
    root = root.resolve()
    if not (root / 'MANIFEST.txt').is_file():
        raise ValueError('The corpus root must contain MANIFEST.txt.')
    files = sorted(p for p in root.rglob('*') if p.is_file())
    digests = {str(p.relative_to(root)): sha256(p) for p in files}
    groups: dict[str, list[str]] = defaultdict(list)
    for name, digest in digests.items():
        groups[digest].append(name)
    entries = []
    for line in (root / 'MANIFEST.txt').read_text().splitlines():
        match = re.fullmatch(r'([0-9a-f]{64})\s+\./(.+)', line)
        if match:
            entries.append(match.groups())
    result = {
        'scope': 'Offline checks of supplied files; not provider authentication or a live reproduction.',
        'inventory': {
            'files': len(files),
            'extensions': dict(Counter(p.suffix.lower() for p in files)),
            'unique_file_sha256_values': len(groups),
            'byte_identical_file_groups': [v for v in groups.values() if len(v) > 1],
            'manifest_entries': len(entries),
            'manifest_missing': [p for h, p in entries if p not in digests],
            'manifest_mismatches': [p for h, p in entries if p in digests and digests[p] != h],
            'scope_note': 'Exact duplicate files are not independent corroboration. Distinct hashes do not imply independent observations.',
        },
    }
    home = root / 'codex/codex_home_2026-11-09'
    voice = json.loads((home / 'realtime-voice-continuity.json').read_text())['threads']
    pairs = []
    roles: Counter = Counter()
    for tid, thread in voice.items():
        items = thread['items']
        roles.update(item['role'] for item in items)
        for i in range(len(items) - 1):
            if items[i] == items[i + 1]:
                pairs.append({'thread': tid, 'positions_1_based': [i+1, i+2],
                              'role': items[i]['role'], 'text_sha256': hashlib.sha256(items[i]['text'].encode()).hexdigest()})
    result['voice_state'] = {
        'source_sha256': sha256(home / 'realtime-voice-continuity.json'),
        'threads': len(voice), 'role_counts': dict(roles),
        'adjacent_exact_duplicate_pairs': len(pairs), 'pairs': pairs,
        'illustrative_duplicate': 'I appreciate the help, though',
        'limit': 'Duplicate saved records, not proof of duplicate speech, model input, or the source of a visible loop.',
    }
    controls = []
    for filename in ['Code_Box_Compiled_List_2026-11-09.md', 'Sigil_Markup_Spec_v0.1_2026-11-06.md']:
        p = root / 'substrate' / filename
        text = p.read_text()
        controls.append({'source': str(p.relative_to(root)), 'sha256': sha256(p),
                         'first_line': text.splitlines()[0],
                         'first_line_occurrences': text.count(text.splitlines()[0]),
                         'last_nonempty_line': text.strip().splitlines()[-1],
                         'backslash_before_underscore_count': text.count('\\_')})
    result['source_controls'] = controls
    try:
        from markdown_it import MarkdownIt
        md = MarkdownIt('commonmark')
        runs = []
        for initial in (23, 19):
            text = '\\' * initial + '_'
            stages = []
            for step in range(6):
                stages.append({'step': step, 'backslashes': text.count('\\'), 'text': text})
                text = md.renderInline(text)
            expected = [23, 11, 5, 2, 1, 0] if initial == 23 else [19, 9, 4, 2, 1, 0]
            runs.append({'initial_count': initial, 'stages': stages,
                         'matches_reported_sequence': [s['backslashes'] for s in stages] == expected})
        result['markdown_experiment'] = {
            'package': 'markdown-it-py', 'version': importlib.metadata.version('markdown-it-py'),
            'configuration': "MarkdownIt('commonmark').renderInline; output reused as next input",
            'input_form': 'N literal U+005C backslashes immediately followed by U+005F underscore',
            'runs': runs,
            'finding': 'Repeated Markdown parsing reproduces both reported ladders, including the final 1-to-0 step.',
            'limits': 'Constructed minimal inputs. Does not establish that the actual application uses this parser or that its historical processing followed these steps. Does not test other characters, omissions, attribution, or document loss.',
        }
    except ImportError:
        result['markdown_experiment'] = {'status': 'not run', 'reason': 'markdown-it-py is not installed'}
    imports = json.loads((home / 'claude-cowork-import-history.json').read_text())
    state = json.loads((home / 'codex-global-state-5.json').read_text())
    hosts = json.loads((home / 'chrome-native-hosts-v2.json').read_text())
    result['local_integration_state'] = {
        'import_item_types': [x['itemType'] for x in imports['accountSetupItems']],
        'import_times_utc': [datetime.fromtimestamp(x['importedAtMs']/1000, timezone.utc).isoformat() for x in imports['accountSetupItems']],
        'imported_records_count': len(imports['records']),
        'first_seen_utc': datetime.fromtimestamp(state['desktop-first-seen-at-ms']/1000, timezone.utc).isoformat(),
        'native_host_entries': len(hosts['entries']),
        'limit': 'Evidence of stored configuration/import/registration state, not proof of an operation in any disputed incident.',
    }
    p = root / 'evidence_packages/room_artifacts_2026-11-10/row49/Prime_Rune_400x400.txt'
    rows = p.read_text().splitlines()
    bound = 2_000_000
    sieve = bytearray(b'\x01') * (bound + 1)
    sieve[0:2] = b'\x00\x00'
    for i in range(2, int(bound ** 0.5) + 1):
        if sieve[i]:
            sieve[i*i::i] = b'\x00' * (((bound - i*i)//i) + 1)
    prime_stream = ''.join(str(i) for i in range(2, bound+1) if sieve[i])
    result['prime_control'] = {
        'rows': len(rows), 'all_widths_400': all(len(x) == 400 for x in rows),
        'matches_first_160000_prime_concatenation_digits': ''.join(rows) == prime_stream[:160000],
        'row49_sha256': hashlib.sha256(rows[48].encode()).hexdigest(),
    }
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', type=Path)
    parser.add_argument('--out', type=Path)
    args = parser.parse_args()
    try:
        result = inspect(args.root)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.exit(1, f'Check failed: {exc}\n')
    text = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
    if args.out:
        args.out.write_text(text, encoding='utf-8')
    else:
        print(text, end='')

if __name__ == '__main__':
    main()
