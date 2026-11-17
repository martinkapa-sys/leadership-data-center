#!/usr/bin/env python3
"""Composite artwork into mockup templates.

  mockup.py designs/<SKU>/print/<SKU>_4x5.jpg [--templates brand/mockups] [--out designs/<SKU>/mockups]

Each template is a pair in brand/mockups/: <name>.png (room/frame photo) and <name>.json:
  {"box": [left, top, right, bottom], "ratio": "4x5", "mat_px": 0, "shadow": true}
"box" is the visible art window inside the frame. Only templates whose "ratio" matches the
art file's ratio are used. Output: <out>/<SKU>_<template>.jpg (2000px long side, web-ready).
"""
import argparse
import glob
import json
import os

from PIL import Image, ImageFilter, ImageOps

Image.MAX_IMAGE_PIXELS = None


def main():
    p = argparse.ArgumentParser()
    p.add_argument("art")
    p.add_argument("--templates", default="brand/mockups")
    p.add_argument("--out")
    a = p.parse_args()

    base = os.path.splitext(os.path.basename(a.art))[0]
    sku, ratio = base.rsplit("_", 1)
    out_dir = a.out or os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(a.art))), "mockups")
    os.makedirs(out_dir, exist_ok=True)
    art = Image.open(a.art).convert("RGB")
    made = []
    for spec_path in sorted(glob.glob(os.path.join(a.templates, "*.json"))):
        spec = json.load(open(spec_path))
        if spec.get("ratio") != ratio:
            continue
        name = os.path.splitext(os.path.basename(spec_path))[0]
        tpl = Image.open(os.path.join(a.templates, name + ".png")).convert("RGB")
        l, t, r, b = spec["box"]
        mat = spec.get("mat_px", 0)
        piece = ImageOps.fit(art, (r - l - 2 * mat, b - t - 2 * mat), Image.LANCZOS)
        if spec.get("shadow"):
            shadow = Image.new("L", tpl.size, 0)
            shadow.paste(90, (l + 6, t + 8, r + 6, b + 8))
            tpl = Image.composite(Image.new("RGB", tpl.size, (0, 0, 0)), tpl,
                                  shadow.filter(ImageFilter.GaussianBlur(10)))
        if mat:
            tpl.paste((250, 250, 248), (l, t, r, b))
        tpl.paste(piece, (l + mat, t + mat))
        tpl.thumbnail((2000, 2000), Image.LANCZOS)
        path = os.path.join(out_dir, f"{sku}_{name}.jpg")
        tpl.save(path, "JPEG", quality=88)
        made.append(path)
    print("\n".join(made) if made else f"No templates with ratio {ratio} in {a.templates}")


if __name__ == "__main__":
    main()
