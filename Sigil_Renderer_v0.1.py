#!/usr/bin/env python3
"""
_l0437 Sigil Markup - Section 5 renderer (spec v0.1).

Implements the validation and rendering contract of section 5 of the
_l0437 Sigil Markup Draft Specification v0.1, using only the spec's own
rules:

  section 1  fenced xml/sigil blocks parsed as XML; malformed input gets a
             diagnostic, never a silent reinterpretation; unresolved
             anchors are warned about, never given invented coordinates.
  section 2  elements, scopes (local/scene/document, default local),
             inheritance document -> scene -> element; duplicate ids and
             unknown references are validation errors.
  section 3  prime-path algorithm: 23x23 rows grid, counterclockwise
             spiral grid, factor paths 1 -> prime factors (ascending, with
             multiplicity) -> n; 1 and 0 special-cased; integers outside
             1..529 are number markers, not plotted paths; explicit
             mirror/rotate transforms apply after the path is computed.
  section 4  room frame 13x13 ft with origin at the geometric center,
             corners at (+-6.5, +-6.5); artwork frame normalized [0,1]
             with (0,0) top-left, y downward; channel colors.
  section 5  the renderer (a) shows the input source or a parse error,
             (b) computes and displays factorizations accurately,
             (c) preserves requested positions and the flame,
             (d) never invents missing coordinates, and
             (e) reports every applied transform and scope.
             Output is reproducible from the same source and version.

Usage:
  sigil_renderer.py INPUT.md [-o OUT.svg] [--report REPORT.txt]
  sigil_renderer.py --selftest
  sigil_renderer.py --proof [-o OUT.svg] [--report REPORT.txt]

Stdlib only. No network, no external actions.
"""

import math
import sys
import xml.etree.ElementTree as ET

# --------------------------------------------------------------------------
# Section 3 arithmetic
# --------------------------------------------------------------------------

def gcd_many(*nums):
    g = 0
    for n in nums:
        g = math.gcd(g, n)
    return g

def factorize(n):
    """Prime factors of n with multiplicity, ascending. n >= 2."""
    out = []
    d = 2
    m = n
    while d * d <= m:
        while m % d == 0:
            out.append(d)
            m //= d
        d += 1 if d == 2 else 2
    if m > 1:
        out.append(m)
    return out

def is_prime(n):
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True

def factor_path(n):
    """Section 3.3: 1 -> prime factors ascending with multiplicity -> n.
    Section 3.4: 1 has no prime factors (path is [1]); 0 has no factor
    path (returns None)."""
    if n == 0:
        return None
    if n == 1:
        return [1]
    return [1] + factorize(n) + [n]

def factorization_str(n):
    fac = factorize(n)
    parts = []
    for p in fac:
        if parts and parts[-1][0] == p:
            parts[-1][1] += 1
        else:
            parts.append([p, 1])
    return " x ".join(str(p) if e == 1 else f"{p}^{e}" for p, e in parts)

# --------------------------------------------------------------------------
# Section 3 grids
# --------------------------------------------------------------------------

def rows_pos(n):
    """Section 3.1: (row, column), both 1-indexed, on the 23x23 grid."""
    return ((n - 1) // 23 + 1, (n - 1) % 23 + 1)

_SPIRAL = {1: (0, 0)}

def _build_spiral(limit):
    x = y = 0
    n = 1
    step = 1
    dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]  # E, N, W, S = counterclockwise
    di = 0
    while n < limit:
        for _ in range(2):  # each segment length occurs twice
            dx, dy = dirs[di % 4]
            di += 1
            for _ in range(step):
                if n >= limit:
                    break
                x += dx
                y += dy
                n += 1
                _SPIRAL[n] = (x, y)
            if n >= limit:
                break
        step += 1

_build_spiral(529)

def spiral_pos(n):
    """Section 3.2: counterclockwise spiral, 1 at (0,0), 2 at (1,0),
    3 at (1,1), 4 at (0,1)."""
    return _SPIRAL[n]

# --------------------------------------------------------------------------
# Parsing and validation (sections 1, 2, 5)
# --------------------------------------------------------------------------

class Diagnostic(Exception):
    pass

NAMED_COLORS = {
    "green": "#3fae5a", "blue": "#3f7fbf", "gold": "#d9a441",
    "violet": "#8a6fd6", "purple": "#8a6fd6", "red": "#d9534f",
    "obsidian": "#101014", "white": "#e8e4d8", "black": "#101014",
}
CHANNELS = {  # section 4
    "green": "carbon / witness / 437", "blue": "silicon / computer / 1109",
    "purple": "subwoofer", "red": "echo",
}
SCOPES = ("local", "scene", "document")

def extract_block(text):
    """Find a fenced ```xml or ```sigil block; fall back to raw XML."""
    lines = text.splitlines()
    in_block = False
    buf = []
    for ln in lines:
        s = ln.strip()
        if not in_block and (s == "```xml" or s == "```sigil"):
            in_block = True
            continue
        if in_block and s == "```":
            return "\n".join(buf)
        if in_block:
            buf.append(ln)
    stripped = text.strip()
    if stripped.startswith("<"):
        return stripped
    raise Diagnostic("no fenced xml/sigil block found in input")

def parse_sigilbook(source):
    try:
        root = ET.fromstring(source)
    except ET.ParseError as e:
        raise Diagnostic(f"XML parse error: {e}")
    if root.tag != "sigilbook":
        raise Diagnostic(f"root element must be <sigilbook>, found <{root.tag}>")
    return root

class Scene:
    def __init__(self, el):
        self.id = el.get("id")
        self.spaces = {}
        self.anchors = {}
        self.runes = []
        self.motifs = []
        self.links = []
        for child in el:
            if child.tag == "space":
                self.spaces[child.get("id")] = child
            elif child.tag == "anchor":
                self.anchors[child.get("id")] = child
            elif child.tag == "rune":
                self.runes.append(child)
            elif child.tag == "motif":
                self.motifs.append(child)
            elif child.tag == "link":
                self.links.append(child)

def resolve_anchor(scene, anchor_id, warnings, errors):
    """Return ('room', x_ft, y_ft) or ('artwork', x, y) or None.
    Never invents coordinates (section 5d)."""
    el = scene.anchors.get(anchor_id)
    if el is None:
        warnings.append(
            f"anchor '{anchor_id}' is referenced but never defined; "
            "left unresolved (no coordinates invented)")
        return None
    frame = el.get("frame")
    space = scene.spaces.get(frame)
    if el.get("x") is not None and el.get("y") is not None:
        return ("artwork", float(el.get("x")), float(el.get("y")))
    if el.get("x-ft") is not None and el.get("y-ft") is not None:
        return ("room", float(el.get("x-ft")), float(el.get("y-ft")))
    zone = el.get("zone")
    if zone and space is not None and frame != "artwork":
        w = float(space.get("width-ft", "0")) / 2.0
        d = float(space.get("depth-ft", "0")) / 2.0
        corners = {
            "upper-right-corner": (w, d), "upper-left-corner": (-w, d),
            "lower-right-corner": (w, -d), "lower-left-corner": (-w, -d),
        }
        if zone in corners:
            x, y = corners[zone]
            return ("room", x, y)
        if zone == "corner":
            warnings.append(
                f"anchor '{anchor_id}': zone 'corner' does not say which "
                "corner; per section 4 its precise coordinates remain "
                "unspecified until measured - left unresolved")
            return None
    warnings.append(
        f"anchor '{anchor_id}' has no usable location; left unresolved")
    return None

def validate(root):
    """Section 2: duplicate ids and unknown references are errors."""
    errors, warnings = [], []
    ids = {}
    for el in root.iter():
        i = el.get("id")
        if i:
            if i in ids:
                errors.append(f"duplicate id '{i}'")
            ids[i] = el.tag
    for scene_el in root.iter("scene"):
        scene = Scene(scene_el)
        known = set(scene.anchors) | {r.get("id") for r in scene.runes} \
            | {m.get("id") for m in scene.motifs} | set(scene.spaces)
        for r in scene.runes:
            at = r.get("at")
            if at and at not in known:
                pass  # unresolved references warn at resolve time (section 1)
            scope = r.get("scope", "local")
            if scope not in SCOPES:
                errors.append(f"rune '{r.get('id')}': unknown scope '{scope}'")
            try:
                int(r.get("number"))
            except (TypeError, ValueError):
                errors.append(f"rune '{r.get('id')}': number must be an integer")
        for lk in scene.links:
            for end in ("from", "to"):
                if lk.get(end) not in known:
                    warnings.append(
                        f"link '{lk.get('kind')}': {end} '{lk.get(end)}' is "
                        "not a defined anchor, rune, or motif in this scene")
    return errors, warnings

# --------------------------------------------------------------------------
# Transforms (section 3.5)
# --------------------------------------------------------------------------

def apply_transforms(points, el, grid_half, report):
    """points: list of (x, y) in grid coordinates centered at 0.
    mirror='vertical' reflects x; rotate-deg rotates counterclockwise.
    Applied after the untransformed path is calculated; reported."""
    rid = el.get("id")
    pts = points
    if el.get("mirror") == "vertical":
        pts = [(-x, y) for x, y in pts]
        report.append(f"transform: rune '{rid}' mirror=vertical applied")
    if el.get("mirror") == "horizontal":
        pts = [(x, -y) for x, y in pts]
        report.append(f"transform: rune '{rid}' mirror=horizontal applied")
    if el.get("rotate-deg"):
        deg = float(el.get("rotate-deg"))
        th = math.radians(deg)
        c, s = math.cos(th), math.sin(th)
        pts = [(x * c - y * s, x * s + y * c) for x, y in pts]
        report.append(f"transform: rune '{rid}' rotate-deg={el.get('rotate-deg')} applied")
    return pts

# --------------------------------------------------------------------------
# SVG rendering
# --------------------------------------------------------------------------

def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))

class Canvas:
    def __init__(self, w, h, bg):
        self.w, self.h, self.parts = w, h, []
        self.parts.append(
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" '
            f'height="{h}" viewBox="0 0 {w} {h}">')
        self.parts.append(f'<rect width="{w}" height="{h}" fill="{bg}"/>')
    def line(self, x1, y1, x2, y2, color, width=1, opacity=1.0, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.parts.append(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{color}" stroke-width="{width}" opacity="{opacity}"{d}/>')
    def polyline(self, pts, color, width=2.5):
        p = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        self.parts.append(
            f'<polyline points="{p}" fill="none" stroke="{color}" '
            f'stroke-width="{width}" stroke-linejoin="round"/>')
    def dot(self, x, y, color, label=None, r=5):
        self.parts.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{color}" '
            f'stroke="#e8e4d8" stroke-width="1"/>')
        if label is not None:
            self.parts.append(
                f'<text x="{x + r + 2:.1f}" y="{y - r:.1f}" fill="{color}" '
                f'font-family="monospace" font-size="11">{esc(label)}</text>')
    def text(self, x, y, s, color="#e8e4d8", size=13, anchor="start",
             family="monospace", weight="normal"):
        self.parts.append(
            f'<text x="{x:.1f}" y="{y:.1f}" fill="{color}" '
            f'font-family="{family}" font-size="{size}" '
            f'font-weight="{weight}" text-anchor="{anchor}">{esc(s)}</text>')
    def build(self):
        self.parts.append("</svg>")
        return "\n".join(self.parts)

def draw_grid_panel(cv, ox, oy, cell, title):
    size = 23 * cell
    cv.text(ox, oy - 10, title, "#e8e4d8", 14, weight="bold")
    for i in range(24):
        cv.line(ox + i * cell, oy, ox + i * cell, oy + size, "#26262e", 1)
        cv.line(ox, oy + i * cell, ox + size, oy + i * cell, "#26262e", 1)

def rows_xy(n, ox, oy, cell):
    r, c = rows_pos(n)
    return (ox + (c - 0.5) * cell, oy + (r - 0.5) * cell)

def spiral_xy(n, ox, oy, cell, half=11):
    x, y = spiral_pos(n)
    return (ox + (x + half + 0.5) * cell, oy + (half - y + 0.5) * cell)

FLAME = "M0,14 C-6,8 -5,2 0,-6 C5,2 6,8 0,14 Z"  # simple flame glyph path

def render(root, source_text):
    errors, warnings = validate(root)
    report = []
    report.append(f"sigilbook id={root.get('id')} version={root.get('version')}")
    palette = "obsidian-gold"
    for st in root.iter("style"):
        palette = st.get("palette", palette)
    report.append(f"style palette={palette} (document default, section 2)")
    bg = "#0b0b10" if "obsidian" in palette else "#141414"
    accent = "#d9a441" if "gold" in palette else "#e8e4d8"

    scenes = [Scene(el) for el in root.iter("scene")]
    cell = 22
    grid_size = 23 * cell
    panel_w = grid_size + 40
    room_w = 340
    width = panel_w * 2 + room_w + 60
    height = grid_size + 330
    cv = Canvas(width, height, bg)

    report_lines_y = grid_size + 90
    # --- factor-path panels, one per layout used -------------------------
    layouts = {}
    for sc in scenes:
        for r in sc.runes:
            layouts.setdefault(r.get("layout", "none"), []).append((sc, r))
    panel_x = {"rows": 20, "spiral": 20 + panel_w}
    drawn = set()
    for layout in ("rows", "spiral"):
        if layout not in layouts:
            continue
        ox = panel_x[layout]
        oy = 50
        title = ("ROWS GRID 23x23 - factor paths" if layout == "rows"
                 else "SPIRAL GRID - factor paths")
        draw_grid_panel(cv, ox, oy, cell, title)
        for sc, r in layouts[layout]:
            drawn.add(r.get("id"))
            n = int(r.get("number"))
            color = NAMED_COLORS.get(r.get("color", ""), accent)
            path = factor_path(n)
            if path is None:
                report.append(f"rune '{r.get('id')}': number 0 has no finite "
                              "prime factorization and cannot have a factor "
                              "path (section 3.4) - not plotted")
                continue
            if n > 529:
                report.append(f"rune '{r.get('id')}': {n} is outside 1..529; "
                              "shown as a number marker, not plotted "
                              "(section 3.4)")
                continue
            if layout == "rows":
                pts = [rows_xy(v, ox, oy, cell) for v in path]
                grid_pts = [(c - 12, 12 - r_) for (r_, c) in
                            (rows_pos(v) for v in path)]
            else:
                pts = [spiral_xy(v, ox, oy, cell) for v in path]
                grid_pts = [spiral_pos(v) for v in path]
            if r.get("mirror") or r.get("rotate-deg"):
                tpts = apply_transforms(grid_pts, r, 11, report)
                if layout == "rows":
                    pts = [(ox + (x + 11 + 0.5) * cell,
                            oy + (11 - y + 0.5) * cell) for x, y in tpts]
                else:
                    pts = [(ox + (x + 11 + 0.5) * cell,
                            oy + (11 - y + 0.5) * cell) for x, y in tpts]
            cv.polyline(pts, color)
            seen = set()
            for v, (px, py) in zip(path, pts):
                if v not in seen:
                    cv.dot(px, py, color, str(v))
                    seen.add(v)
            report.append(
                f"rune '{r.get('id')}': {n} = {factorization_str(n)}; "
                f"path {'-'.join(str(v) for v in path)}; layout={layout}; "
                f"color={r.get('color')} "
                f"(channel: {CHANNELS.get(r.get('color',''), 'none')}); "
                f"scope={r.get('scope', 'local')}; at={r.get('at')}")
    # runes with layout=none or unplottable -> number markers in report
    for sc in scenes:
        for r in sc.runes:
            if r.get("id") in drawn:
                continue
            n = int(r.get("number"))
            kind = "prime" if is_prime(n) else "composite"
            extra = ""
            if n > 529:
                extra = "; outside 1..529, number marker only (section 3.4)"
            report.append(
                f"rune '{r.get('id')}': {n} ({kind}) = "
                f"{factorization_str(n) if n >= 2 else n}; "
                f"layout={r.get('layout', 'none')} - no path plotted{extra}; "
                f"scope={r.get('scope', 'local')}; at={r.get('at')}")

    # section 1: a referenced-but-undefined anchor (e.g. 'computer') must
    # produce a warning, never invented coordinates
    for sc in scenes:
        refs = [r.get("at") for r in sc.runes] + [m.get("at") for m in sc.motifs]
        for ref in refs:
            if ref and ref not in sc.anchors and ref not in warnings:
                warnings.append(
                    f"anchor '{ref}' is referenced but never defined; "
                    "left unresolved (section 1)")
    # --- room panel --------------------------------------------------------
    rx = 20 + panel_w * 2
    ry = 50
    cv.text(rx, ry - 10, "ROOM FRAME (ft, origin center)", "#e8e4d8", 14,
            weight="bold")
    for sc in scenes:
        for sid, space in sc.spaces.items():
            if space.get("kind") != "square":
                continue
            w_ft = float(space.get("width-ft", "13"))
            d_ft = float(space.get("depth-ft", "13"))
            scale = room_w / w_ft
            cx, cy = rx + room_w / 2, ry + room_w / 2
            cv.parts.append(
                f'<rect x="{rx}" y="{ry}" width="{room_w}" height="{room_w}" '
                f'fill="none" stroke="{accent}" stroke-width="1.5"/>')
            cv.line(cx - 6, cy, cx + 6, cy, "#666", 1)
            cv.line(cx, cy - 6, cx, cy + 6, "#666", 1)
            def room_xy(x_ft, y_ft):
                return (cx + x_ft * scale, cy - y_ft * scale)
            placed = {}
            for aid in sc.anchors:
                pos = resolve_anchor(sc, aid, warnings, errors)
                if pos is None:
                    continue
                if pos[0] == "room":
                    px, py = room_xy(pos[1], pos[2])
                    placed[aid] = (px, py)
                    cv.dot(px, py, accent, aid, r=4)
                else:
                    report.append(
                        f"anchor '{aid}': artwork frame "
                        f"({pos[1]}, {pos[2]}) = {pos[1] * 100:.1f}%, "
                        f"{pos[2] * 100:.1f}% of the image (section 4); "
                        "not a room position")
                    inset = room_w // 2
                    ix0, iy0 = rx, ry + room_w + 46
                    if not any(p.startswith("artwork-inset") for p in drawn):
                        drawn.add("artwork-inset")
                        cv.text(ix0, iy0 - 8, "ARTWORK FRAME (normalized)",
                                "#e8e4d8", 12, weight="bold")
                        cv.parts.append(
                            f'<rect x="{ix0}" y="{iy0}" width="{inset}" '
                            f'height="{inset}" fill="none" '
                            f'stroke="{accent}" stroke-width="1"/>')
                    ix = ix0 + pos[1] * inset
                    iy = iy0 + pos[2] * inset
                    placed[aid] = (ix, iy)
                    cv.dot(ix, iy, NAMED_COLORS["purple"], aid, r=4)
            for m in sc.motifs:
                target = placed.get(m.get("at"))
                report.append(
                    f"motif '{m.get('id')}': kind={m.get('kind')} "
                    f"at={m.get('at')} scope={m.get('scope', 'local')}")
                if target and m.get("kind") == "flame":
                    x, y = target
                    # glyph drawn inward from the corner so it stays
                    # inside the room frame
                    cv.parts.append(
                        f'<path d="{FLAME}" transform="translate({x - 11:.1f},'
                        f'{y + 3:.1f}) scale(1.5)" fill="#e07b39" '
                        f'stroke="#d9a441" stroke-width="0.7"/>')
                    cv.text(x - 14, y + 34, "flame", "#e07b39", 11,
                            anchor="end")
            for lk in sc.links:
                report.append(
                    f"link: {lk.get('from')} -> {lk.get('to')} "
                    f"kind={lk.get('kind')} (declared relation only; "
                    "implies no unmeasured causation, section 2)")
                a, b = placed.get(lk.get("from")), placed.get(lk.get("to"))
                if a and b:
                    cv.line(a[0], a[1], b[0], b[1], "#3f7fbf", 1.5,
                            opacity=0.8, dash="5,4")
    # --- report panel ------------------------------------------------------
    cv.text(20, grid_size + 70, "RENDER REPORT (section 5)", accent, 14,
            weight="bold")
    y = report_lines_y
    import textwrap
    for ln in report:
        for seg in textwrap.wrap(ln, 148) or [""]:
            cv.text(20, y, seg, "#c9c4b4", 11.5)
            y += 17
    for wtext in warnings:
        cv.text(20, y, "WARNING: " + wtext, "#e0a13e", 11.5)
        y += 17
    for etext in errors:
        cv.text(20, y, "ERROR: " + etext, "#d9534f", 11.5)
        y += 17
    cv.text(20, y + 8,
            "Decorative lines are illustrations, not measured room "
            "acoustics (section 5).", "#8a8676", 11)
    full_report = report + [f"WARNING: {w}" for w in warnings] + \
        [f"ERROR: {e}" for e in errors]
    return cv.build(), full_report

def render_document(text):
    """Returns (svg_text, report_lines). On a parse failure, returns a
    diagnostic SVG and report (section 5a: show the source or the error)."""
    try:
        source = extract_block(text)
        root = parse_sigilbook(source)
    except Diagnostic as d:
        cv = Canvas(900, 220, "#0b0b10")
        cv.text(20, 40, "PARSE DIAGNOSTIC (section 5a)", "#d9534f", 15,
                weight="bold")
        cv.text(20, 75, str(d), "#e8e4d8", 12.5)
        cv.text(20, 110, "Input source as received:", "#d9a441", 12.5)
        y = 135
        for ln in text.splitlines()[:4]:
            cv.text(20, y, ln[:110], "#8a8676", 11)
            y += 16
        return cv.build(), [f"DIAGNOSTIC: {d}"]
    return render(root, source)

# --------------------------------------------------------------------------
# Section 3 test values (the 14 verified checks) and the proof comparison
# --------------------------------------------------------------------------

def selftest():
    checks = []
    def chk(name, ok):
        checks.append((name, ok))
    chk("path(132) = 1-2-2-3-11-132", factor_path(132) == [1, 2, 2, 3, 11, 132])
    chk("437 = 19 x 23", factorize(437) == [19, 23])
    chk("156 = 2^2 x 3 x 13", factorize(156) == [2, 2, 3, 13])
    chk("273 = 3 x 7 x 13", factorize(273) == [3, 7, 13])
    chk("481 = 13 x 37", factorize(481) == [13, 37])
    chk("gcd(156,273) = 39", gcd_many(156, 273) == 39)
    chk("gcd(156,481) = 13", gcd_many(156, 481) == 13)
    chk("gcd(273,481) = 13", gcd_many(273, 481) == 13)
    chk("gcd(156,273,481,437) = 1", gcd_many(156, 273, 481, 437) == 1)
    chk("39 is composite", not is_prime(39) and 39 > 1)
    chk("437 is composite", not is_prime(437))
    chk("13 is prime", is_prime(13))
    chk("1109 is prime", is_prime(1109))
    chk("spiral anchors 1(0,0) 2(1,0) 3(1,1) 4(0,1)",
        spiral_pos(1) == (0, 0) and spiral_pos(2) == (1, 0)
        and spiral_pos(3) == (1, 1) and spiral_pos(4) == (0, 1))
    return checks

# Proof render (2026-11-06) geometry, read from the proof image itself:
# rows grid (row, column) for every plotted vertex; spiral (x, y) anchors.
PROOF_ROWS = {
    437: {1: (1, 1), 19: (1, 19), 23: (1, 23), 437: (19, 23)},
    156: {1: (1, 1), 2: (1, 2), 3: (1, 3), 13: (1, 13), 156: (7, 18)},
    273: {1: (1, 1), 3: (1, 3), 7: (1, 7), 13: (1, 13), 273: (12, 20)},
    481: {1: (1, 1), 13: (1, 13), 37: (2, 14), 481: (21, 21)},
}
PROOF_SPIRAL_156 = {1: (0, 0), 2: (1, 0), 3: (1, 1), 13: (2, 2)}

def proof_checks():
    out = []
    for n, verts in PROOF_ROWS.items():
        ok = all(rows_pos(v) == rc for v, rc in verts.items())
        out.append((f"proof rows geometry for {n}", ok))
    ok = all(spiral_pos(v) == xy for v, xy in PROOF_SPIRAL_156.items())
    out.append(("proof spiral geometry for 156 (anchors 1,2,3,13)", ok))
    x156, y156 = spiral_pos(156)
    out.append((f"proof spiral 156 lands lower-left ({x156},{y156})",
                x156 < 0 and y156 < 0))
    return out

PROOF_INPUT = """```xml
<sigilbook id="_l0437" version="0.1">
  <style palette="obsidian-gold"/>
  <scene id="proof">
    <space id="room" kind="square" width-ft="13" depth-ft="13" origin="center"/>
    <anchor id="origin" frame="room" x-ft="0" y-ft="0"/>
    <rune id="carbon" number="437" color="green" at="origin" layout="rows" scope="scene"/>
    <rune id="bridge-rows" number="156" color="gold" at="origin" layout="rows" scope="scene"/>
    <rune id="violet" number="273" color="violet" at="origin" layout="rows" scope="scene"/>
    <rune id="red" number="481" color="red" at="origin" layout="rows" scope="scene"/>
    <rune id="bridge" number="156" color="gold" at="origin" layout="spiral" scope="local"/>
  </scene>
</sigilbook>
```"""

def main(argv):
    args, opts = [], {}
    it = iter(range(1, len(argv)))
    for i in it:
        a = argv[i]
        if a.startswith("--"):
            if "=" in a:
                k, v = a.split("=", 1)
                opts[k] = v
            elif a in ("--out", "--report") and i + 1 < len(argv):
                opts[a] = argv[i + 1]
                next(it)
            else:
                opts[a] = True
        else:
            args.append(a)
    if "--selftest" in opts or (not args and "--proof" not in opts):
        lines = []
        ok_all = True
        for name, ok in selftest():
            lines.append(f"{'PASS' if ok else 'FAIL'}  {name}")
            ok_all = ok_all and ok
        for name, ok in proof_checks():
            lines.append(f"{'PASS' if ok else 'FAIL'}  {name}")
            ok_all = ok_all and ok
        lines.append("ALL CHECKS PASS" if ok_all else "SOME CHECKS FAILED")
        print("\n".join(lines))
        return 0 if ok_all else 1
    if "--proof" in opts:
        text = PROOF_INPUT
    else:
        with open(args[0], "r", encoding="utf-8") as f:
            text = f.read()
    svg, report = render_document(text)
    out = opts.get("--out", "sigil_render.svg")
    if out is True:
        out = "sigil_render.svg"
    with open(out, "w", encoding="utf-8") as f:
        f.write(svg)
    rep = ["SECTION 5 RENDER REPORT", ""] + report
    if "--report" in opts:
        rp = opts["--report"]
        if rp is True:
            rp = "sigil_report.txt"
        with open(rp, "w", encoding="utf-8") as f:
            f.write("\n".join(rep) + "\n")
    print("\n".join(rep))
    print(f"\n[svg written to {out}]")
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
