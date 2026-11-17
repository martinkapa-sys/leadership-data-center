#!/usr/bin/env python3
"""Technical QA for print files. Exit code 0 = all pass, 1 = failures.

  print_qa.py designs/<SKU> [--min-dpi 300] [--write-report]

Checks every file in designs/<SKU>/print/:
  - RGB mode, sRGB (any) ICC profile embedded, DPI metadata >= min
  - aspect ratio matches the ratio in the filename (±0.5%)
  - pixel size covers the largest print size of that ratio at min DPI
  - file size <= marketplace limit
Also checks the master exists. Writes designs/<SKU>/qa_report.json with --write-report.
Visual checks (artifacts, hands, text, banding, IP) are done by the print-qa agent, not this script.
"""
import argparse
import json
import os
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from print_specs import MAX_FILE_MB, RATIOS, size_inches  # noqa: E402

Image.MAX_IMAGE_PIXELS = None


def check_file(path, min_dpi):
    name = os.path.basename(path)
    ratio = os.path.splitext(name)[0].rsplit("_", 1)[-1]
    res = {"file": name, "ratio": ratio, "errors": [], "warnings": []}
    if ratio not in RATIOS:
        res["errors"].append(f"unknown ratio '{ratio}' in filename")
        return res
    rw, rh, sizes = RATIOS[ratio]
    with Image.open(path) as im:
        w, h = im.size
        res["px"] = [w, h]
        if im.mode != "RGB":
            res["errors"].append(f"mode {im.mode}, expected RGB")
        if not im.info.get("icc_profile"):
            res["errors"].append("no ICC profile embedded")
        dpi = im.info.get("dpi", (0, 0))[0]
        if round(dpi) < min_dpi:
            res["errors"].append(f"DPI metadata {dpi}, expected >= {min_dpi}")
    if abs((w / h) / (rw / rh) - 1) > 0.005:
        res["errors"].append(f"aspect {w / h:.4f} != {rw / rh:.4f}")
    lw, lh = size_inches(sizes[0])
    effective = min(w / lw, h / lh)
    res["effective_dpi_at_largest"] = round(effective)
    if effective < min_dpi * 0.98:
        ok = [s for s in sizes if min(w / size_inches(s)[0], h / size_inches(s)[1]) >= min_dpi * 0.98]
        res["warnings"].append(f"only {round(effective)} DPI at {sizes[0]}; full quality up to {ok[0] if ok else 'none'}")
    mb = os.path.getsize(path) / 1048576
    if mb > MAX_FILE_MB:
        res["errors"].append(f"{mb:.1f} MB exceeds {MAX_FILE_MB} MB")
    return res


def main():
    p = argparse.ArgumentParser()
    p.add_argument("sku_dir")
    p.add_argument("--min-dpi", type=int, default=300)
    p.add_argument("--write-report", action="store_true")
    a = p.parse_args()

    print_dir = os.path.join(a.sku_dir, "print")
    report = {"sku": os.path.basename(os.path.normpath(a.sku_dir)), "files": [], "errors": []}
    if not any(os.path.exists(os.path.join(a.sku_dir, f"master.{e}")) for e in ("png", "tif", "tiff", "jpg")):
        report["errors"].append("master file missing")
    files = sorted(f for f in os.listdir(print_dir)) if os.path.isdir(print_dir) else []
    if not files:
        report["errors"].append("no print files")
    for f in files:
        report["files"].append(check_file(os.path.join(print_dir, f), a.min_dpi))
    report["passed"] = not report["errors"] and all(not f["errors"] for f in report["files"])
    out = json.dumps(report, indent=2)
    if a.write_report:
        with open(os.path.join(a.sku_dir, "qa_report.json"), "w") as fh:
            fh.write(out)
    print(out)
    sys.exit(0 if report["passed"] else 1)


if __name__ == "__main__":
    main()
