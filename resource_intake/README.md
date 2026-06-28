# resource_intake

The raw inbox. Drop anything here and let `playbooks/ingest.md` file it:

- Manuals / spec-sheet PDFs
- Photos of model plates, serial stickers, filter end-caps
- Receipts and order-confirmation emails/PDFs (purchase date, price, seller)
- Saved web pages or pasted Amazon / retailer listings
- Quick notes

The ingest playbook reads each artifact, extracts citable facts into the right
`items/`/`systems/` file (with source + confidence), keeps the artifact as a reference,
and clears it from here.

> Intake artifacts are gitignored — they're your private documents. Only this README is tracked.
