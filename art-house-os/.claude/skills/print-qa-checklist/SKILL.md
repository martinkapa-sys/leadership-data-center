---
name: print-qa-checklist
description: Pass/fail checklist for print files, technical and visual. Use before any design is listed.
---
## Automated (`python3 scripts/print_qa.py designs/<SKU> --write-report`)
RGB · ICC embedded · DPI ≥ 300 · exact aspect ratio · enough pixels for the largest size · ≤ 20 MB.

## Visual (open each file)
- [ ] Subject intact in every crop; nothing important within 3% of the edge (home printers/frames trim).
- [ ] No AI artifacts: hands, faces, eyes, warped architecture, melted text, repeated patterns, seams.
- [ ] No banding in gradients, no halos from upscaling, no JPEG blocking at 100% zoom.
- [ ] No watermark, signature, or stray text.
- [ ] Colours match the brief palette; not oversaturated (prints darker than screens — avoid crushed shadows).
- [ ] Reads well small (thumbnail) and large.
Any unchecked box = fail, with a specific fix instruction.
