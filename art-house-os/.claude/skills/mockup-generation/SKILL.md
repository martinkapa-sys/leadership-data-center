---
name: mockup-generation
description: Create lifestyle and frame mockups for listings and social. Use when preparing listing images.
---
- Templates live in `brand/mockups/<name>.png` + `<name>.json` ({"box":[l,t,r,b],"ratio":"4x5","mat_px":0,"shadow":true}).
  Source room photos from licensed mockup packs or Canva; record licences in `brand/mockups/LICENSES.md`.
- `python3 scripts/mockup.py designs/<SKU>/print/<SKU>_<ratio>.jpg`
- Listing image order: 1 hero room mockup · 2 close-up/detail · 3 frame on plain wall · 4 size guide graphic · 5 "what you get" (files + ratios) · 6+ alternate rooms.
- Match room style to the brief's target room. Keep the hero mockup consistent across a collection.
