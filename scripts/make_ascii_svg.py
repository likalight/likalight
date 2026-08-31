#!/usr/bin/env python3
"""Turn a photo into a self-typing ASCII portrait SVG.

    pip install pillow numpy opencv-python-headless rembg onnxruntime
    python scripts/make_ascii_svg.py photo.jpg ascii.svg --crop 0.33,0.13,0.71,0.57

The first run downloads a ~176 MB background-removal model, once.

Pipeline, and why each stage is there:

  rembg cut-out     everything outside the subject is forced to white, which
                    maps to the blank end of the ramp. Skip it and the
                    background fills with @ and drowns the portrait.
  bilateral filter  smooths skin while keeping edges.
  CLAHE             local contrast per tile. Global autocontrast leaves a
                    flatly-lit face as one flat tone.
  darkening curve   (v/255)^1.7. Without it the face comes out washed out
                    and featureless; this is what makes glasses, brows and
                    lips survive the downscale.
  map to ramp       the leading space clears the background to nothing.

The font is embedded rather than named. The grid bakes in an advance width
of exactly 0.600 em, which Liberation/DejaVu/Noto Mono honour but Consolas
-- what Windows lands on -- does not, at about 0.55. Without the embedded
subset a Windows visitor sees the portrait some 7% narrower.
"""
import argparse
import os
import sys

import cv2
import numpy as np
from PIL import Image
from rembg import remove

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fontkit import load  # noqa: E402

RAMP = " .`:-=+*cs#%@"          # bright/sparse -> dark/dense
CHAR_W = 7.74                   # 0.600 em at font-size 12.9
FONT_SIZE = 12.9
LINE_H = 15
ROW_DELAY = 0.09


def prep(path, clip, blur, curve, tile):
    """Cut out the subject, then flatten it to a contrast-shaped greyscale."""
    source = Image.open(path).convert("RGBA")
    cut = remove(source)
    alpha = np.array(cut.split()[-1])
    white = Image.new("RGBA", cut.size, (255, 255, 255, 255))
    gray = np.array(Image.alpha_composite(white, cut).convert("L"))
    gray = cv2.bilateralFilter(gray, 11, blur, blur)
    gray = cv2.createCLAHE(clipLimit=clip, tileGridSize=(tile, tile)).apply(gray)
    gray = (255.0 * (gray / 255.0) ** curve).astype(np.uint8)  # darkening curve
    gray[alpha < 20] = 255                                    # background to blank
    return Image.fromarray(gray)


def to_lines(img, cols, gamma, crop=None):
    if crop:
        w, h = img.size
        left, top, right, bottom = crop
        img = img.crop((int(w * left), int(h * top), int(w * right), int(h * bottom)))
    w, h = img.size
    rows = int(cols * (h / float(w)) * 0.48)   # monospace cells are ~2x tall as wide
    img = img.resize((cols, rows), Image.LANCZOS)
    pixels = list(img.getdata())
    depth = len(RAMP)
    lines = []
    for row in range(rows):
        line = "".join(
            RAMP[min(depth - 1, int((1 - pixels[row * cols + col] / 255.0) ** gamma * depth))]
            for col in range(cols)
        )
        lines.append(line.rstrip())
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    return lines


def build_svg(lines, out_path, cols):
    """Each row is a clipPath whose rect wipes open, with a block as cursor.

    Rows stagger top to bottom and every animation is fill="freeze", so the
    portrait types itself once and stops. No looping.
    """
    pad = 14
    width = int(cols * CHAR_W + pad * 2)
    height = len(lines) * LINE_H + pad * 2
    face = (
        "@font-face{font-family:'JBM';font-style:normal;font-weight:400;"
        "src:url(data:font/woff2;base64,%s) format('woff2')}" % load("ramp")
    )
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" '
        'viewBox="0 0 %d %d" role="img" aria-label="ASCII portrait">'
        % (width, height, width, height),
        "<style>%s.a{fill:#57606a;font-family:'JBM',ui-monospace,SFMono-Regular,"
        "Menlo,Consolas,monospace}"
        "@media(prefers-color-scheme:dark){.a{fill:#c9d1d9}}</style>" % face,
    ]
    for i, line in enumerate(lines):
        y = pad + i * LINE_H
        begin = "%.2fs" % (i * ROW_DELAY)
        end = "%.2fs" % ((i + 1) * ROW_DELAY)
        run = max(len(line), 1) * CHAR_W
        safe = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        parts.append(
            '<clipPath id="c%d"><rect x="%d" y="%d" height="%d" width="0">'
            '<animate attributeName="width" from="0" to="%.1f" begin="%s" '
            'dur="%.2fs" fill="freeze"/></rect></clipPath>'
            % (i, pad, y, LINE_H, run, begin, ROW_DELAY)
        )
        parts.append(
            '<g clip-path="url(#c%d)"><text xml:space="preserve" x="%d" y="%.1f" '
            'class="a" font-size="%s">%s</text></g>'
            % (i, pad, y + 11.2, FONT_SIZE, safe)
        )
        parts.append(
            '<rect y="%d" width="6" height="12" class="a" opacity="0">'
            '<animate attributeName="x" from="%d" to="%.1f" begin="%s" dur="%.2fs" '
            'fill="freeze"/><set attributeName="opacity" to="0.8" begin="%s"/>'
            '<set attributeName="opacity" to="0" begin="%s"/></rect>'
            % (y + 1, pad, pad + run, begin, ROW_DELAY, begin, end)
        )
    parts.append("</svg>")
    with open(out_path, "w", encoding="utf-8") as handle:
        handle.write("".join(parts))
    return width, height


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("photo")
    ap.add_argument("out", nargs="?", default="ascii.svg")
    ap.add_argument("--cols", type=int, default=90)
    ap.add_argument("--gamma", type=float, default=1.35)
    ap.add_argument("--clip", type=float, default=3.0)
    ap.add_argument("--blur", type=int, default=50)
    ap.add_argument("--tile", type=int, default=8,
                    help="CLAHE tile grid; finer tiles rescue a flatly-lit face")
    ap.add_argument("--curve", type=float, default=1.7,
                    help="darkening curve exponent; lower for an already-dark photo")
    ap.add_argument("--crop", default=None,
                    help="left,top,right,bottom as fractions of the image")
    args = ap.parse_args()

    crop = [float(v) for v in args.crop.split(",")] if args.crop else None
    lines = to_lines(prep(args.photo, args.clip, args.blur, args.curve, args.tile), args.cols, args.gamma, crop)
    print("\n".join(lines))
    width, height = build_svg(lines, args.out, args.cols)
    print("\nwrote %s  %d rows, %dx%d, types for %.1fs"
          % (args.out, len(lines), width, height, len(lines) * ROW_DELAY + ROW_DELAY))


if __name__ == "__main__":
    main()
