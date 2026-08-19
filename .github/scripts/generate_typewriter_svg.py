import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "..", "assets", "typewriter.svg")

lines = [
    "Competitive Programmer",
    "Building AI Systems",
    "Backend Developer",
    "LeetCode Guardian",
    "Turning Ideas Into Code",
    "Code. Create. Evolve."
]

TYPE_SPEED = 0.06
HOLD_TIME = 1.2
ERASE_SPEED = 0.04
PAUSE_TIME = 0.3

CHAR_W = 14.45
START_X = 270

total_dur = 0
for line in lines:
    total_dur += len(line) * TYPE_SPEED
    total_dur += HOLD_TIME
    total_dur += len(line) * ERASE_SPEED
    total_dur += PAUSE_TIME

svg = []
svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 50" width="100%" height="50">')
svg.append('<style>')
svg.append('@import url("https://fonts.googleapis.com/css2?family=Fira+Code:wght@600&amp;display=swap");')
svg.append('.text { font-family: "Fira Code", monospace; font-size: 24px; fill: #00E5FF; font-weight: 600; }')
svg.append('.prompt { font-family: "Fira Code", monospace; font-size: 24px; fill: #7d8590; font-weight: 600; }')
svg.append('.cursor { fill: #00E5FF; }')
svg.append('</style>')

svg.append('<rect width="800" height="50" fill="transparent"/>')
svg.append(f'<text x="250" y="35" class="prompt">&gt;</text>')

clip_values = []
clip_times = []
cursor_values = []
cursor_times = []

t_current = 0.0

clip_values.append("0")
clip_times.append("0")
cursor_values.append(str(START_X))
cursor_times.append("0")

for line in lines:
    L = len(line)
    
    # End of typing
    t_current += L * TYPE_SPEED
    clip_values.append(str(L * CHAR_W))
    clip_times.append(f"{t_current / total_dur:.4f}")
    cursor_values.append(str(START_X + L * CHAR_W))
    cursor_times.append(f"{t_current / total_dur:.4f}")
    
    # End of holding
    t_current += HOLD_TIME
    clip_values.append(str(L * CHAR_W))
    clip_times.append(f"{t_current / total_dur:.4f}")
    cursor_values.append(str(START_X + L * CHAR_W))
    cursor_times.append(f"{t_current / total_dur:.4f}")
    
    # End of erasing
    t_current += L * ERASE_SPEED
    clip_values.append("0")
    clip_times.append(f"{t_current / total_dur:.4f}")
    cursor_values.append(str(START_X))
    cursor_times.append(f"{t_current / total_dur:.4f}")
    
    # End of pausing
    t_current += PAUSE_TIME
    clip_values.append("0")
    clip_times.append(f"{t_current / total_dur:.4f}")
    cursor_values.append(str(START_X))
    cursor_times.append(f"{t_current / total_dur:.4f}")

# Ensure last time is exactly 1
clip_times[-1] = "1"
cursor_times[-1] = "1"

clip_val_str = ";".join(clip_values)
clip_time_str = ";".join(clip_times)
cursor_val_str = ";".join(cursor_values)
cursor_time_str = ";".join(cursor_times)

svg.append('<clipPath id="type-clip">')
svg.append(f'  <rect x="{START_X}" y="0" width="0" height="50">')
svg.append(f'    <animate attributeName="width" values="{clip_val_str}" keyTimes="{clip_time_str}" dur="{total_dur:.3f}s" calcMode="linear" repeatCount="indefinite" />')
svg.append('  </rect>')
svg.append('</clipPath>')

svg.append('<g clip-path="url(#type-clip)">')

t_current = 0.0
for i, line in enumerate(lines):
    L = len(line)
    dur_this = L * TYPE_SPEED + HOLD_TIME + L * ERASE_SPEED + PAUSE_TIME
    
    t_start = t_current
    t_end = t_current + dur_this
    
    t_start_norm = t_start / total_dur
    t_end_norm = t_end / total_dur
    
    # We use discrete display animation so they don't overlap
    if i == 0:
        times = [0, t_end_norm, 1]
        vals = ["1", "0", "0"]
    elif i == len(lines) - 1:
        times = [0, t_start_norm, 1]
        vals = ["0", "1", "1"]
    else:
        times = [0, t_start_norm, t_end_norm, 1]
        vals = ["0", "1", "0", "0"]
        
    times_str = ";".join([f"{x:.4f}" for x in times])
    vals_str = ";".join(vals)
    
    svg.append(f'  <text x="{START_X}" y="35" class="text" opacity="0">')
    svg.append(f'    <animate attributeName="opacity" values="{vals_str}" keyTimes="{times_str}" dur="{total_dur:.3f}s" calcMode="discrete" repeatCount="indefinite" />')
    svg.append(f'    {line}')
    svg.append('  </text>')
    
    t_current += dur_this

svg.append('</g>')

svg.append(f'<rect x="{START_X}" y="12" width="12" height="28" class="cursor">')
svg.append(f'  <animate attributeName="x" values="{cursor_val_str}" keyTimes="{cursor_time_str}" dur="{total_dur:.3f}s" calcMode="linear" repeatCount="indefinite" />')
svg.append(f'  <animate attributeName="opacity" values="1;0;1;0" keyTimes="0;0.5;0.51;1" dur="0.8s" repeatCount="indefinite" />')
svg.append('</rect>')

svg.append('</svg>')

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w") as f:
    f.write("\n".join(svg))
