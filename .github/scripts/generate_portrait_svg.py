import os
import sys
import html
import base64
import struct

HERE = os.path.dirname(os.path.abspath(__file__))
IN_FILE = os.path.join(HERE, "..", "..", "assets", "ascii-art_img.png")
OUT_FILE = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "..", "assets", "portrait.svg")

with open(IN_FILE, "rb") as f:
    data = f.read()

png_w, png_h = struct.unpack('>LL', data[16:24])
b64_data = base64.b64encode(data).decode('utf-8')

PAD = 20
TITLEBAR_H = 30
STATUS_H = 30

ART_W = 1000
ART_H = int(ART_W * (png_h / png_w))

CANVAS_W = int(ART_W + PAD * 2)
CANVAS_H = int(TITLEBAR_H + ART_H + STATUS_H + PAD)

BG = "#0d1117"
BG2 = "#111722"
FRAME = "#30363d"
TITLE_TEXT = "#7d8590"
INK = "#c9d1d9"
CURSOR = "#c9d1d9"

parts = []
parts.append(
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{CANVAS_W}" height="{CANVAS_H}" '
    f'viewBox="0 0 {CANVAS_W} {CANVAS_H}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">'
)
parts.append('<defs>'
             f'<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">'
             f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/>'
             f'</linearGradient></defs>')

parts.append(f'<rect width="{CANVAS_W}" height="{CANVAS_H}" rx="12" fill="url(#bg)"/>')
parts.append(f'<rect x="0.5" y="0.5" width="{CANVAS_W-1}" height="{CANVAS_H-1}" rx="12" '
             f'fill="none" stroke="{FRAME}" stroke-width="1"/>')

parts.append(f'<line x1="0" y1="{TITLEBAR_H}" x2="{CANVAS_W}" y2="{TITLEBAR_H}" stroke="{FRAME}"/>')
for i, dotcol in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
    parts.append(f'<circle cx="{PAD + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{dotcol}"/>')
parts.append(f'<text x="{CANVAS_W/2}" y="{TITLEBAR_H/2 + 4}" fill="{TITLE_TEXT}" font-size="12" '
             f'text-anchor="middle">akassh@github: ~$ ./portrait.sh</text>')

art_top = TITLEBAR_H + PAD * 0.35

TOTAL_DUR = 2.0
parts.append(
    f'<clipPath id="reveal">'
    f'<rect x="{PAD}" y="{art_top}" height="{ART_H}" width="0">'
    f'<animate attributeName="width" from="0" to="{ART_W}" begin="0.5s" '
    f'dur="{TOTAL_DUR}s" fill="freeze"/></rect></clipPath>'
)

parts.append(f'<g clip-path="url(#reveal)">')
parts.append(f'<image href="data:image/png;base64,{b64_data}" x="{PAD}" y="{art_top}" width="{ART_W}" height="{ART_H}" preserveAspectRatio="xMidYMid meet" />')
parts.append(f'</g>')

status_line_y = TITLEBAR_H + ART_H + PAD * 0.35
status_y = status_line_y + 19
parts.append(f'<line x1="0" y1="{status_line_y:.1f}" x2="{CANVAS_W}" y2="{status_line_y:.1f}" stroke="{FRAME}"/>')
parts.append(f'<text x="{PAD}" y="{status_y:.1f}" fill="{TITLE_TEXT}" font-size="13">'
             f'akassh@github:~$ whoami <tspan fill="{INK}">Akassh M</tspan></text>')
parts.append(f'<rect x="{PAD+210}" y="{status_y-12:.1f}" width="8" height="14" fill="{CURSOR}">'
             f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.51;1" '
             f'dur="1s" repeatCount="indefinite"/></rect>')

parts.append("</svg>")

os.makedirs(os.path.dirname(OUT_FILE), exist_ok=True)
with open(OUT_FILE, "w", encoding="utf-8") as f:
    f.write("".join(parts))
