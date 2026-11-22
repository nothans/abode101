# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "pymupdf==2.1",
# ]
# ///
"""Make a scanned PDF searchable with no installs: render pages, OCR with Windows' built-in
engine (winocr.ps1, Windows PowerShell 5.1), and lay the words back as an invisible text layer.

usage: uv run ocr_pdf.py <in.pdf> <out.pdf> [dpi]

uv installs PyMuPDF from the header above. Scans are left untouched; only a text layer is added.
Work files (PNG renders, OCR JSON) go to ./work-<name>/ next to this script and are reused on rerun.
"""
import json
import os
import subprocess
import sys

import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
src, dst = sys.argv[1], sys.argv[2]
dpi = int(sys.argv[3]) if len(sys.argv) > 3 else 250
work = os.path.join(HERE, 'work-' + os.path.splitext(os.path.basename(src))[0])
png_dir, json_dir = os.path.join(work, 'png'), os.path.join(work, 'json')
os.makedirs(png_dir, exist_ok=True)

doc = pymupdf.open(src)
print('pages', len(doc))
for i, page in enumerate(doc):
    out = os.path.join(png_dir, f'p{i:04d}.png')
    if not os.path.exists(out):
        page.get_pixmap(dpi=dpi).save(out)
print('rendered')

if not os.path.isdir(json_dir) or len(os.listdir(json_dir)) < len(doc):
    r = subprocess.run(['powershell.exe', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File',
                        os.path.join(HERE, 'winocr.ps1'), '-InDir', png_dir, '-OutDir', json_dir],
                       capture_output=True, text=True)
    print(r.stdout[-2000:]); print(r.stderr[-2000:])
    if r.returncode != 0:
        sys.exit('ocr failed')


def as_list(x):
    if x is None:
        return []
    return x if isinstance(x, list) else [x]


words_total = 0
for i, page in enumerate(doc):
    with open(os.path.join(json_dir, f'p{i:04d}.json'), encoding='utf-8-sig') as f:
        data = json.load(f)
    sx = page.rect.width / data['width']
    sy = page.rect.height / data['height']
    page.wrap_contents()  # scans often leave a page-sized cm on the CTM; bracket it so our text lands on the page
    tw = pymupdf.TextWriter(page.rect)
    for line in as_list(data.get('lines')):
        for w in as_list(line.get('words')):
            t = w['t']
            if not t.strip():
                continue
            x0, y0 = w['x'] * sx, w['y'] * sy
            bw, bh = w['w'] * sx, w['h'] * sy
            if bw <= 0 or bh <= 0:
                continue
            fs = bh
            tl = pymupdf.get_text_length(t, fontname='helv', fontsize=fs)
            if tl > bw and tl > 0:
                fs = fs * bw / tl
            tw.append(pymupdf.Point(x0, y0 + bh * 0.85), t, fontsize=fs)
            words_total += 1
    tw.write_text(page, render_mode=3)
doc.save(dst, garbage=3, deflate=True, deflate_images=False)
print('words placed', words_total, '->', dst, os.path.getsize(dst), 'bytes')
