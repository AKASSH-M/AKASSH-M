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

duration_per_line = 3.5
total_duration = duration_per_line * len(lines)
char_width = 14.45  # Approximate width for Fira Code at 24px

svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 50" width="100%" height="50">']
svg.append('<style>')
svg.append('@import url("https://fonts.googleapis.com/css2?family=Fira+Code:wght@600&amp;display=swap");')
svg.append('.text { font-family: "Fira Code", monospace; font-size: 24px; fill: #00E5FF; font-weight: 600; }')
svg.append('.prompt { font-family: "Fira Code", monospace; font-size: 24px; fill: #7d8590; font-weight: 600; }')
svg.append('</style>')

svg.append('<rect width="800" height="50" fill="transparent"/>')

svg.append('<text x="250" y="35" class="prompt">&gt;</text>')

for i, line in enumerate(lines):
    line_width = len(line) * char_width
    
    # Calculate the keyTimes over the total duration
    t_start = i / len(lines)
    t_type_end = (i + 0.25) / len(lines)
    t_hold_end = (i + 0.75) / len(lines)
    t_erase_end = (i + 0.90) / len(lines)
    t_next = (i + 1.0) / len(lines)
    
    # We need 0 everywhere else
    values = f"0;0;{line_width};{line_width};0;0;0"
    
    kt = []
    if t_start > 0:
        kt.append("0")
    kt.append(f"{t_start:.4f}")
    kt.append(f"{t_type_end:.4f}")
    kt.append(f"{t_hold_end:.4f}")
    kt.append(f"{t_erase_end:.4f}")
    if t_next < 1.0:
        kt.append(f"{t_next:.4f}")
        kt.append("1")
    else:
        kt.append("1")
    
    # ensure we have 7 values in keyTimes if we have 7 values
    # Let's dynamically build the values and keyTimes arrays
    
    val_arr = []
    kt_arr = []
    
    if t_start > 0:
        val_arr.append("0")
        kt_arr.append("0")
        
    val_arr.extend(["0", str(line_width), str(line_width), "0"])
    kt_arr.extend([f"{t_start:.4f}", f"{t_type_end:.4f}", f"{t_hold_end:.4f}", f"{t_erase_end:.4f}"])
    
    if t_next < 1.0:
        val_arr.extend(["0", "0"])
        kt_arr.extend([f"{t_next:.4f}", "1"])
    else:
        val_arr.append("0")
        kt_arr.append("1")
    
    val_str = ";".join(val_arr)
    kt_str = ";".join(kt_arr)
    
    if t_start == 0:
        kt_arr_op = [0, t_erase_end, 1]
        val_arr_op = [1, 0, 0]
    else:
        kt_arr_op = [0, t_start, t_erase_end, 1]
        val_arr_op = [0, 1, 0, 0]
        
    kt_str_op = ";".join(f"{x:.4f}" for x in kt_arr_op)
    val_str_op = ";".join(str(x) for x in val_arr_op)
    
    svg.append(f'<clipPath id="clip{i}">')
    svg.append(f'  <rect x="270" y="0" width="0" height="50">')
    svg.append(f'    <animate attributeName="width" values="{val_str}" keyTimes="{kt_str}" dur="{total_duration}s" fill="freeze" repeatCount="indefinite" />')
    svg.append(f'  </rect>')
    svg.append(f'</clipPath>')
    
    svg.append(f'<text x="270" y="35" class="text" clip-path="url(#clip{i})" opacity="0">')
    svg.append(f'  <animate attributeName="opacity" values="{val_str_op}" keyTimes="{kt_str_op}" calcMode="discrete" dur="{total_duration}s" repeatCount="indefinite" />')
    svg.append(f'  {line}')
    svg.append(f'</text>')

svg.append('<rect x="270" y="12" width="12" height="28" fill="#00E5FF">')
values = []
keyTimes = []
for i, line in enumerate(lines):
    line_width = len(line) * char_width
    t_start = i / len(lines)
    t_type_end = (i + 0.25) / len(lines)
    t_hold_end = (i + 0.75) / len(lines)
    t_erase_end = (i + 0.90) / len(lines)
    
    values.extend([0, line_width, line_width, 0])
    keyTimes.extend([t_start, t_type_end, t_hold_end, t_erase_end])

values_str = ";".join([str(v+270) for v in values]) + f";{270}"
keyTimes[-1] = 0.999 # just avoiding 1
keyTimes_str = ";".join([f"{kt:.4f}" for kt in keyTimes]) + ";1"

svg.append(f'<animate attributeName="x" values="{values_str}" keyTimes="{keyTimes_str}" dur="{total_duration}s" repeatCount="indefinite"/>')
svg.append(f'<animate attributeName="opacity" values="1;0;1;0" keyTimes="0;0.5;0.51;1" dur="0.8s" repeatCount="indefinite"/>')
svg.append('</rect>')

svg.append('</svg>')

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w") as f:
    f.write("\\n".join(svg))
