# pdf-text

Read a PDF's text layer when extracting facts for the base: dump pages in reading order, or search for a term and see the page it lands on.
This is what the ingest playbook means by "read the manual"; it replaces the `pdftotext` binary the playbook used to assume.

## Use

```powershell
python tools/pdf-text/pdf_text.py info   "references/<slug>/manual.pdf"
python tools/pdf-text/pdf_text.py search "references/<slug>/manual.pdf" "CR2032"
python tools/pdf-text/pdf_text.py dump   "references/<slug>/manual.pdf" --pages 10-12
```

- `info` prints the page count, the embedded metadata, and whether the file has a text layer.
- `search` prints every hit with its PDF page number and surrounding text, so a Specs row can cite `manual p.<n>`.
- `dump` prints the text of the chosen pages (all pages if none given).
- A scan with no text layer gets a hint to run `tools/pdf-ocr/` first.

Page numbers are PDF pages, 1-based. When a manual carries its own printed numbering, cite that and put the PDF page in parentheses, as the reference docs do.

## Needs

Python with PyMuPDF (`pip install pymupdf`).
