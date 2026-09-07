# tools

Small, dependency-light helpers the playbooks call. Each folder has its own README with usage and requirements.

- [`pdf-text/`](pdf-text/README.md): read a PDF's text layer (info, dump pages, search a term with page numbers). The "read the manual" step of `playbooks/ingest.md`.
- [`pdf-ocr/`](pdf-ocr/README.md): give a scanned PDF a searchable text layer on Windows with nothing to install (PyMuPDF plus the built-in Windows OCR engine). Run it before `pdf-text` on a scan.
- [`artifact-meta/`](artifact-meta/README.md): show or set the embedded metadata of a filed artifact (JPEG, PNG, PDF, MP4, MP3) with one vocabulary, without re-encoding. The "Filing the artifact" step of `playbooks/ingest.md`.

Requirements: Python 3 with `piexif`, `Pillow`, and `PyMuPDF` (`pip install piexif pillow pymupdf`); ffmpeg on the PATH (or `FFMPEG=<path>`) for audio and video tags; Windows PowerShell 5.1 for the OCR engine.
