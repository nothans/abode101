"""Read a PDF's text layer for fact extraction: dump pages, or search for a term and see where it lands.

usage:
  python pdf_text.py info   <file.pdf>                     pages, metadata, and whether a text layer exists
  python pdf_text.py dump   <file.pdf> [--pages 3-5,12]    text of the pages (all pages by default), reading order
  python pdf_text.py search <file.pdf> <term> [--context 80]  every hit with its page number and surrounding text

A PDF with no text layer (a scan) prints a hint to run tools/pdf-ocr first. Page numbers are PDF pages (1-based);
cite the printed page number from the page itself when the manual has its own numbering.
Needs PyMuPDF (pip install pymupdf).
"""
import argparse
import re
import sys

import fitz  # PyMuPDF


def pages_arg(spec, n):
    if not spec:
        return list(range(n))
    out = []
    for part in spec.split(','):
        part = part.strip()
        if '-' in part:
            a, b = part.split('-', 1)
            out.extend(range(int(a) - 1, min(int(b), n)))
        else:
            out.append(int(part) - 1)
    return [p for p in out if 0 <= p < n]


def has_text(doc):
    sample = [doc[i] for i in range(0, len(doc), max(1, len(doc) // 8))]
    return sum(len(p.get_text().strip()) for p in sample) > 40 * len(sample)


def main():
    # PDF text and metadata carry characters the Windows console code page cannot encode.
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('action', choices=['info', 'dump', 'search'])
    ap.add_argument('file')
    ap.add_argument('term', nargs='?')
    ap.add_argument('--pages')
    ap.add_argument('--context', type=int, default=80)
    a = ap.parse_args()
    doc = fitz.open(a.file)
    textual = has_text(doc)
    if a.action == 'info':
        print(f'pages        {len(doc)}')
        for k, v in doc.metadata.items():
            if v:
                print(f'{k:12} {v}')
        print(f'text layer   {"yes" if textual else "no (a scan: run tools/pdf-ocr/ocr_pdf.py first)"}')
        return
    if not textual:
        sys.exit('no text layer: run tools/pdf-ocr/ocr_pdf.py on this file first')
    if a.action == 'dump':
        for i in pages_arg(a.pages, len(doc)):
            print(f'===== pdf page {i + 1} =====')
            print(doc[i].get_text('text', sort=True))
        return
    if not a.term:
        sys.exit('search needs a term')
    pat = re.compile(re.escape(a.term), re.I)
    hits = 0
    for i in pages_arg(a.pages, len(doc)):
        text = doc[i].get_text('text', sort=True)
        flat = re.sub(r'\s+', ' ', text)
        for m in pat.finditer(flat):
            hits += 1
            s, e = max(0, m.start() - a.context), min(len(flat), m.end() + a.context)
            print(f'pdf p.{i + 1}: ...{flat[s:e]}...')
    print(f'{hits} hit(s) for "{a.term}"')


if __name__ == '__main__':
    main()
