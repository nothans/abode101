# pdf-ocr

Make a scanned PDF searchable on Windows with nothing to install.
Pages are rendered with PyMuPDF, read by the Windows built-in OCR engine, and the words are laid back onto the original pages as an invisible text layer.
The scan is left untouched, so the file looks identical and grows by roughly the size of the text.

## Use

```powershell
uv run tools/pdf-ocr/ocr_pdf.py "<in.pdf>" "<out.pdf>" [dpi]
```

- Default render is 250 dpi. Go to 300 for small print.
- Renders and OCR results are cached in `tools/pdf-ocr/work-<name>/` (gitignored), so a rerun only redoes the merge. Delete the folder when the PDF is done.
- Needs [uv](https://docs.astral.sh/uv/), which installs the pinned PyMuPDF from the script's header, and Windows PowerShell 5.1 (`powershell.exe`), which every Windows 11 machine has. The engine must have an English language pack, which the default install does.

## Files

- `ocr_pdf.py` is the driver: render, call the OCR script, place the text, save.
- `winocr.ps1` runs `Windows.Media.Ocr` over a folder of PNGs and writes one JSON per page with words and pixel boxes.

## Notes

- Old scans often leave a page-sized `cm` on the content stream. The driver wraps the existing content in `q ... Q` first, or the new text lands off the page and nothing is searchable.
- Text is placed with a `TextWriter` per page (one font resource, one stream). Placing words one `insert_text` call at a time doubled a 5 MB manual; this keeps it near the original size.
- The text layer is OCR. A part number with a doubtful digit should be checked against the page image.
- A 118-page scanned manual (about 28,000 words) takes a few minutes end to end.
