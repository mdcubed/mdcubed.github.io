"""Recolour the MD³ cube mark into the navy / gold palette.

Reads the original vector artwork (assets/logo/md3-mark-original.svg) and
writes the variants used by the website and for slides/posters:

    md3-mark-dark.svg     cream + gold, transparent — for navy backgrounds
    md3-mark-light.svg    navy + bronze, transparent — for white/cream backgrounds
    md3-mark-solid.svg    filled navy cube — works on any background (favicon)
    md3-mark-blue.svg     navy + blue, transparent — the website's light theme
    md3-lockup-*.svg      mark + group name, horizontal and stacked

Run:  python scripts/make_logo.py
"""
import re
from pathlib import Path

LOGO = Path(__file__).resolve().parents[1] / "assets" / "logo"
src = (LOGO / "md3-mark-original.svg").read_text()

# Geometry only: the cube, the letters, the ΔG glyphs, the curve and arrowhead.
cube_faces = re.findall(r'<polygon class="st[09]" points="([^"]+)"', src)  # top, left, right
outline = re.search(r'<polygon class="st3" points="([^"]+)"', src).group(1)
edges = re.search(r'<path class="st3" d="([^"]+)"', src).group(1)
letters = re.findall(r'<path class="st8" d="([^"]+)"', src)
delta = re.search(r'<path class="st6" d="([^"]+)"', src).group(1)
gee = re.search(r'<path class="st5" d="([^"]+)"', src).group(1)
curve = re.search(r'<path class="st2" d="([^"]+)"', src).group(1)
arrow = re.search(r'<path class="st7" d="([^"]+)"', src).group(1)

NAVY, DEEP, CARD, MID = "#0B1A33", "#071226", "#112A52", "#1B3B6E"
GOLD, GOLD_LIGHT, BRONZE, CREAM = "#D4AF5A", "#E9CF8A", "#8A6420", "#F3EEDF"

VARIANTS = {
    #         top     left    right   line   letters accent
    "dark":  ("none", "none", MID,    CREAM, CREAM,  GOLD),
    "light": ("none", "none", GOLD_LIGHT, NAVY, NAVY, BRONZE),
    "solid": (CARD,   NAVY,   MID,    GOLD,  CREAM,  GOLD),
    "blue":  ("none", "none", "#C9D8EE", NAVY, NAVY, "#2A5A99"),  # light theme of the website
}


def mark(variant):
    """Inner SVG for the cube in its native coordinates (crop: 155 29 624 716)."""
    top, left, right, line, text, accent = VARIANTS[variant]
    return f'''<g>
    <polygon points="{cube_faces[0]}" fill="{top}"/>
    <polygon points="{cube_faces[1]}" fill="{left}"/>
    <polygon points="{cube_faces[2]}" fill="{right}"/>
    <g fill="none" stroke="{line}" stroke-width="19" stroke-linecap="round" stroke-linejoin="round">
      <polygon points="{outline}"/>
      <path d="{edges}"/>
    </g>
    <g fill="{text}">{"".join(f'<path d="{d}"/>' for d in letters)}</g>
    <g fill="{accent}">
      <path fill-rule="evenodd" d="{delta}"/>
      <path d="{gee}"/>
      <path d="{arrow}" stroke="{accent}" stroke-width="7" stroke-linejoin="round"/>
    </g>
    <path d="{curve}" fill="none" stroke="{accent}" stroke-width="13" stroke-linecap="round"/>
  </g>'''


BOX = (155, 29, 624, 716)  # tight crop around the cube, stroke included
FONT = "'Trebuchet MS', 'Lucida Grande', Arial, sans-serif"


def write(name, body, w, h):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
           f'width="{w}" height="{h}" role="img" aria-label="MD³ Group">\n  {body}\n</svg>\n')
    (LOGO / name).write_text(svg)
    print("wrote", name)


for v in VARIANTS:
    x, y, w, h = BOX
    write(f"md3-mark-{v}.svg", f'<g transform="translate({-x} {-y})">{mark(v)}</g>', w, h)

# Lockups. Text stays live (system fonts), so it remains editable.
for v, (name_c, sub_c, rule_c) in {"dark": (CREAM, "#B9C4D8", GOLD),
                                   "light": (NAVY, "#3A4A66", BRONZE)}.items():
    x, y, w, h = BOX
    s = 300 / h  # mark drawn 300 tall
    mw = w * s
    horiz = f'''<g transform="scale({s:.4f}) translate({-x} {-y})">{mark(v)}</g>
  <rect x="{mw + 44:.0f}" y="62" width="3" height="176" fill="{rule_c}"/>
  <text x="{mw + 80:.0f}" y="138" font-family="{FONT}" font-weight="700" font-size="92" letter-spacing="1" fill="{name_c}">MD<tspan font-size="54" dy="-34">3</tspan><tspan dy="34"> Group</tspan></text>
  <text x="{mw + 82:.0f}" y="204" font-family="Arial, Helvetica, sans-serif" font-size="38" fill="{sub_c}">Mechanistic Drug Design and Discovery</text>'''
    write(f"md3-lockup-horizontal-{v}.svg", horiz, 1100, 300)

    s2 = 420 / h
    cx = 400
    stacked = f'''<g transform="translate({cx - w * s2 / 2:.1f} 0) scale({s2:.4f}) translate({-x} {-y})">{mark(v)}</g>
  <rect x="{cx - 28}" y="462" width="56" height="3" fill="{rule_c}"/>
  <text x="{cx}" y="540" text-anchor="middle" font-family="{FONT}" font-weight="700" font-size="60" fill="{name_c}">Mechanistic Drug Design</text>
  <text x="{cx}" y="612" text-anchor="middle" font-family="{FONT}" font-weight="700" font-size="60" fill="{name_c}">and Discovery Group</text>'''
    write(f"md3-lockup-stacked-{v}.svg", stacked, 800, 650)
