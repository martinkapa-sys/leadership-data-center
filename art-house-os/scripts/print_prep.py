#!/usr/bin/env python3
"""Turn a master image into print-ready files for every ratio.

  print_prep.py designs/<SKU>/master.png [--ratios 2x3,3x4,4x5,11x14,iso] [--max-long-px 10800]
                [--focus 0.5,0.5] [--format jpg|png]

- center-crops (or crops around --focus, as fractions of width,height) to each ratio
- resizes with Lanczos to the largest supported print size at 300 DPI
- converts to RGB, embeds an sRGB ICC profile and 300 DPI metadata
- writes designs/<SKU>/print/<SKU>_<ratio>.<ext> and prints a JSON summary

Upscaling quality: if the master needs > 2x enlargement for a ratio the summary flags it;
run an AI upscaler (e.g. Real-ESRGAN via the Replicate connector) on the master first.
"""
import argparse
import io
import json
import os
import sys

from PIL import Image, ImageCms

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from print_specs import DPI, MAX_FILE_MB, RATIOS, target_pixels  # noqa: E402

Image.MAX_IMAGE_PIXELS = None
SRGB = ImageCms.ImageCmsProfile(ImageCms.createProfile("sRGB")).tobytes()


def crop_to_ratio(img, rw, rh, fx, fy):
    W, H = img.size
    target = rw / rh
    if W / H > target:          # too wide
        nw = round(H * target)
        left = min(max(round(fx * W - nw / 2), 0), W - nw)
        return img.crop((left, 0, left + nw, H))
    nh = round(W / target)      # too tall
    top = min(max(round(fy * H - nh / 2), 0), H - nh)
    return img.crop((0, top, W, top + nh))


def save(img, path, fmt):
    kw = {"dpi": (DPI, DPI), "icc_profile": SRGB}
    if fmt == "jpg":
        for q in (95, 92, 90, 87, 85):
            buf = io.BytesIO()
            img.save(buf, "JPEG", quality=q, subsampling=0, **kw)
            if buf.tell() <= MAX_FILE_MB * 1024 * 1024 or q == 85:
                with open(path, "wb") as f:
                    f.write(buf.getvalue())
                return q
    img.save(path, "PNG", optimize=True, **kw)
    return None


def main():
    p = argparse.ArgumentParser()
    p.add_argument("master")
    p.add_argument("--ratios", default=",".join(RATIOS))
    p.add_argument("--max-long-px", type=int, default=None)
    p.add_argument("--focus", default="0.5,0.5")
    p.add_argument("--format", choices=["jpg", "png"], default="jpg")
    a = p.parse_args()

    sku_dir = os.path.dirname(os.path.abspath(a.master))
    sku = os.path.basename(sku_dir)
    out_dir = os.path.join(sku_dir, "print")
    os.makedirs(out_dir, exist_ok=True)
    fx, fy = (float(v) for v in a.focus.split(","))

    src = Image.open(a.master)
    if src.mode != "RGB":
        src = src.convert("RGB")
    summary = []
    for ratio in a.ratios.split(","):
        rw, rh, sizes = RATIOS[ratio]
        cropped = crop_to_ratio(src, rw, rh, fx, fy)
        tw, th = target_pixels(ratio, a.max_long_px)
        scale = tw / cropped.width
        out = cropped.resize((tw, th), Image.LANCZOS)
        path = os.path.join(out_dir, f"{sku}_{ratio}.{a.format}")
        q = save(out, path, a.format)
        summary.append({"ratio": ratio, "file": os.path.relpath(path), "px": [tw, th], "sizes": sizes,
                        "upscale_factor": round(scale, 2), "needs_ai_upscale": scale > 2,
                        "jpeg_quality": q, "mb": round(os.path.getsize(path) / 1048576, 1)})
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
