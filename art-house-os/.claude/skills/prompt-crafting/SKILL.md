---
name: prompt-crafting
description: House method for writing image-generation prompts, choosing models, and tracking seeds and versions. Use when generating artwork.
---
## Model choice (via Replicate / fal.ai)
- Painterly, photographic, abstract → FLUX (pro/dev) class models.
- Typography / quote prints → Ideogram class models (accurate text).
- Vector / flat illustration / line art → Recraft class models (SVG output).
- Upscaling → Real-ESRGAN / Clarity-style upscalers to ≥ 7200 px long side.

## Prompt structure
`<subject>, <composition: centred with generous margin>, <medium/technique>, <palette from brief (named colours)>, <lighting/mood>, <texture: paper grain, brush>, gallery-quality fine art print`
- Pull style vocabulary from `brand/style-guide.md` — never an artist's name.
- Negative: text, watermark, signature, frame, border, blurry, extra fingers, distorted, logo.
- Generate at the brief's master ratio (usually 4:5 or 2:3) with headroom for crops.

## Record in `designs/<SKU>/prompt.md`
model + version, full prompt, negative, seed(s), params, chosen variant + reason, post-edits made.
