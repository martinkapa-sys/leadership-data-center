"""Shared print specifications: ratio sets and the sizes each file must support at 300 DPI."""

DPI = 300
MAX_FILE_MB = 20  # Etsy per-file limit for digital downloads

# ratio name -> (width units, height units, list of sizes in inches the file must cover, largest first)
RATIOS = {
    "2x3": (2, 3, ["24x36", "20x30", "16x24", "12x18", "8x12", "4x6"]),
    "3x4": (3, 4, ["18x24", "12x16", "9x12", "6x8"]),
    "4x5": (4, 5, ["16x20", "8x10", "4x5"]),
    "11x14": (11, 14, ["11x14"]),
    "iso": (1, 2 ** 0.5, ["A1", "A2", "A3", "A4", "A5"]),
}

ISO_INCHES = {"A1": (23.39, 33.11), "A2": (16.54, 23.39), "A3": (11.69, 16.54), "A4": (8.27, 11.69), "A5": (5.83, 8.27)}


def size_inches(label: str):
    if label in ISO_INCHES:
        return ISO_INCHES[label]
    w, h = label.split("x")
    return float(w), float(h)


def target_pixels(ratio: str, max_long_px: int | None = None):
    """Pixel size for a ratio's largest print size at DPI, optionally capped on the long side."""
    w_in, h_in = size_inches(RATIOS[ratio][2][0])
    w, h = round(w_in * DPI), round(h_in * DPI)
    if max_long_px and max(w, h) > max_long_px:
        k = max_long_px / max(w, h)
        w, h = round(w * k), round(h * k)
    return w, h
