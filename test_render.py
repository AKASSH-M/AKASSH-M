import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, 'assets', 'ascii-art.txt'), 'r') as f:
    lines = f.readlines()[:40]

img = Image.new('RGB', (1200, 800), color='#0d1117')
d = ImageDraw.Draw(img)
try:
    font = ImageFont.truetype("DejaVuSansMono.ttf", 10)
except:
    font = ImageFont.load_default()

y = 10
for line in lines:
    d.text((10, y), line.strip(), font=font, fill='#0d1117', stroke_width=1, stroke_fill='#c9d1d9')
    y += 12

img.save(os.path.join(HERE, 'assets', 'test_render_stroke.png'))
