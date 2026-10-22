# -*- coding: utf-8 -*-
"""Shrink an oversized GIF under Zenn's 3MB limit by subsampling frames,
reducing the palette, and (if needed) downscaling. Re-compress only -- no resim."""
import sys, os
from PIL import Image, ImageSequence

path = r"E:\NovaSolver\zenn-content\images\reaction-diffusion\slider-anim.gif"
TARGET = 2.7 * 1024 * 1024

im = Image.open(path)
frames = [f.convert("RGB") for f in ImageSequence.Iterator(im)]
dur = im.info.get("duration", 100)
n0 = len(frames); w0, h0 = frames[0].size
print(f"original: {n0} frames {w0}x{h0} {os.path.getsize(path)/1024/1024:.2f}MB dur={dur}")

def save(frames, dur, colors, scale):
    fr = frames
    if scale != 1.0:
        fr = [f.resize((int(w0*scale), int(h0*scale)), Image.LANCZOS) for f in frames]
    fr = [f.convert("P", palette=Image.ADAPTIVE, colors=colors) for f in fr]
    fr[0].save(path, save_all=True, append_images=fr[1:], duration=dur, loop=0, optimize=True)
    return os.path.getsize(path)

# try progressively stronger compression until under target
for step, colors, scale in [(2, 128, 1.0), (2, 96, 0.9), (3, 96, 0.85), (3, 64, 0.8), (4, 64, 0.75)]:
    sub = frames[::step]
    sz = save(sub, dur*step, colors, scale)
    print(f"  step={step} colors={colors} scale={scale}: {len(sub)} frames -> {sz/1024/1024:.2f}MB")
    if sz <= TARGET:
        print("OK under 2.7MB"); break
print("final:", os.path.getsize(path)/1024/1024, "MB")
