# References

Manuals, spec sheets, listings, receipts, photos, warranties: the artifacts the base's facts cite.

## Where things go
- **Artifacts** live in a folder per item or system: `references/<slug>/` (the slug of the `items/` or `systems/` file they support).
  A multi-file artifact (a listing's photos, a receipt's pages) gets its own subfolder, e.g. `references/pinball-star-trek-tng/listing-pinside-219928/`.
  File names say what the file is (`manual-williams-1991.pdf`, `03-playfield-from-above.jpg`), never the source's random name; the original name goes in the EXIF comment or the reference doc.
  Photos carry their description in EXIF (title, subject, keywords, comment, artist) so a file found on its own still says what it is.
- **Reference docs** are Markdown beside the folders, `references/<slug>-<what>.md`, one per artifact set: what it is, how it was made usable (OCR, page map), what it proves, and a file index.
  They carry `type: reference` frontmatter and cite the artifact as their source.
- `resource_intake/` is the inbox only. The ingest playbook reads a drop, files the facts, moves the artifact here, and leaves the inbox empty.
- The naming rules and the embedded-metadata fields per format (JPEG, PNG, PDF, MP4, MP3) are in `playbooks/ingest.md`, section "Filing the artifact"; the tool that writes them is `tools/artifact-meta/artifact_meta.py` in the hans repo.

> Artifact files are gitignored in the public framework; only this README is tracked there. In the private house repo everything here is backed up.
> The house's own list of reference docs lives in the root `index.md` under References, not here (this file publishes with the framework).
