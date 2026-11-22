# artifact-meta

Show or set the embedded metadata of a knowledge-base artifact, one vocabulary across formats, without re-encoding the content.
Part of the Abode 101 framework: the ingest playbook files every artifact under `references/<slug>/` with these seven fields inside it, so a file found on its own still says what it is.

## Use

```powershell
uv run tools/artifact-meta/artifact_meta.py show "<file>"
uv run tools/artifact-meta/artifact_meta.py set "<file>" --title "<item> listing photo 13: backbox boards" `
  --description "Backbox open: the PinSound RocketCPU lower left, ..." `
  --subject "<item>, <marketplace> ad <id>, seller photo" `
  --keywords "<category>;<item>;<marketplace> listing;backbox" `
  --author "seller, <marketplace> ad <id>" --comment "Original file: <name as received>.jpg" `
  --date 2026-09-06
```

Add `--out <file>` to write a tagged copy and leave the original alone.

## Fields and where they land

| Field | JPEG (EXIF) | PNG (text chunks) | PDF (info) | MP4 / M4A / MOV | MP3 (ID3v2.3) |
|---|---|---|---|---|---|
| title | XPTitle | Title | Title | title | title |
| description | ImageDescription, UserComment | Description | Subject | description | comment |
| subject | XPSubject | Subject | (joined into Subject) | show | album |
| keywords | XPKeywords | Keywords | Keywords | keywords | (joined into comment) |
| author | Artist | Author | Author | artist | artist |
| comment | XPComment | Comment | (joined into Keywords) | comment | comment |
| date | DateTimeOriginal, only if absent | Creation Time | CreationDate, only if absent | date | date |

- JPEG: piexif inserts the EXIF block, the image data is untouched. The XP fields are what Windows Explorer shows as Title, Subject, Tags, Comments.
- PNG: the pixels are rewritten losslessly with the text chunks added. Existing chunks are kept.
- PDF: an incremental save appends the new info dictionary; the pages are untouched.
- MP4 and MP3: ffmpeg stream-copies into a new container with the tags; nothing is re-encoded. ffmpeg comes from `FFMPEG=<path>` or the PATH.

## Needs

[uv](https://docs.astral.sh/uv/), which installs the pinned `piexif`, `Pillow`, and `PyMuPDF` from the script's header on first run, plus ffmpeg for audio and video.
