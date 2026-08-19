import os
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

total_dur = 0
for line in lines:
    total_dur += len(line) * TYPE_SPEED
    total_dur += HOLD_TIME
    total_dur += len(line) * ERASE_SPEED
    total_dur += PAUSE_TIME

print(f"Total duration: {total_dur:.3f}s")
