#!/usr/bin/env python3
"""
Generate device frame template PNGs for both platforms:
  - assets/device_frame_android.png  (Pixel-style, centered hole-punch camera)
  - assets/device_frame_ios.png      (iPhone-style, Dynamic Island pill)
Each is a standalone device image (not positioned on canvas); compose.py positions
it dynamically based on text height.
"""

import os
from PIL import Image, ImageDraw, ImageChops

# ── Device dimensions (shared) ──────────────────────────────────────
DEVICE_W = 1030
DEVICE_H = 2800           # tall enough to bleed off any canvas
DEVICE_CORNER_R = 77
BEZEL = 15
SCREEN_CORNER_R = 62

SCREEN_W = DEVICE_W - 2 * BEZEL
SCREEN_H = DEVICE_H - 2 * BEZEL

ASSETS = os.path.join(os.path.dirname(__file__), "assets")


def _base_frame():
    """Device body + transparent screen cutout, shared by both platforms."""
    frame = Image.new("RGBA", (DEVICE_W, DEVICE_H), (0, 0, 0, 0))
    fd = ImageDraw.Draw(frame)

    # Device body (dark grey outer, darker inner)
    fd.rounded_rectangle([0, 0, DEVICE_W - 1, DEVICE_H - 1],
                         radius=DEVICE_CORNER_R, fill=(30, 30, 30, 255))
    fd.rounded_rectangle([1, 1, DEVICE_W - 2, DEVICE_H - 2],
                         radius=DEVICE_CORNER_R - 1, fill=(20, 20, 20, 255))

    # Screen cutout (transparent)
    cutout = Image.new("L", (DEVICE_W, DEVICE_H), 255)
    ImageDraw.Draw(cutout).rounded_rectangle(
        [BEZEL, BEZEL, BEZEL + SCREEN_W, BEZEL + SCREEN_H],
        radius=SCREEN_CORNER_R, fill=0)
    frame.putalpha(ImageChops.multiply(frame.getchannel("A"), cutout))

    # Side buttons
    btn = (25, 25, 25, 255)
    fd2 = ImageDraw.Draw(frame)
    fd2.rounded_rectangle([DEVICE_W, 340, DEVICE_W + 4, 460], radius=2, fill=btn)  # power
    fd2.rounded_rectangle([-4, 280, 0, 360], radius=2, fill=btn)                   # vol up
    fd2.rounded_rectangle([-4, 380, 0, 460], radius=2, fill=btn)                   # vol down
    fd2.rounded_rectangle([-4, 180, 0, 220], radius=2, fill=btn)                   # silent
    return frame


def generate_android():
    frame = _base_frame()
    # Centered hole-punch front camera
    hp_d, hp_top = 34, 22
    hp_x = (DEVICE_W - hp_d) // 2
    hp_y = BEZEL + hp_top
    ImageDraw.Draw(frame).ellipse([hp_x, hp_y, hp_x + hp_d, hp_y + hp_d], fill=(0, 0, 0, 255))
    out = os.path.join(ASSETS, "device_frame_android.png")
    frame.save(out, "PNG")
    print(f"✓ {out} ({DEVICE_W}×{DEVICE_H}) — Android hole-punch")


def generate_ios():
    frame = _base_frame()
    # Dynamic Island pill
    di_w, di_h, di_top = 130, 38, 14
    di_x = (DEVICE_W - di_w) // 2
    di_y = BEZEL + di_top
    ImageDraw.Draw(frame).rounded_rectangle(
        [di_x, di_y, di_x + di_w, di_y + di_h], radius=di_h // 2, fill=(0, 0, 0, 255))
    out = os.path.join(ASSETS, "device_frame_ios.png")
    frame.save(out, "PNG")
    print(f"✓ {out} ({DEVICE_W}×{DEVICE_H}) — iPhone Dynamic Island")


if __name__ == "__main__":
    generate_android()
    generate_ios()
