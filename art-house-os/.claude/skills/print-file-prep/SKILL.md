---
name: print-file-prep
description: Prepare print-ready files from a master: ratios, sizes, DPI, colour profile, file limits. Use after the master artwork is final.
---
1. Master must be ≥ 7200 px on the long side (24×36 in @ 300 DPI = 7200×10800). Upscale first if not.
2. `python3 scripts/print_prep.py designs/<SKU>/master.png [--focus x,y]` — creates 2x3, 3x4, 4x5, 11x14, ISO files.
   Use `--focus` when the subject is off-centre so crops keep it. Use `--max-long-px` only to meet file-size limits.
3. If any ratio reports `needs_ai_upscale: true`, upscale the master with an AI upscaler and rerun.
4. Files are sRGB JPEG (or PNG for flat graphics), 300 DPI metadata, ≤ 20 MB (Etsy limit; script lowers JPEG quality to fit).
5. Sizes covered per ratio are listed in `scripts/print_specs.py`; they go into the listing's size guide.
