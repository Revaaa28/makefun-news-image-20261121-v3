#!/usr/bin/env python3
"""Entry point: validate the shipped entry.png and copy it to the
output directory named by MAKEFUN_OUTPUT_DIR (default /output).

draw.py is the source of the image; this script is stdlib-only and
fails loudly if the image is not exactly 1024x1024 or exceeds 1 MiB.
"""
import os
import shutil
import struct
import sys

MAX_BYTES = 1024 * 1024  # 1 MiB
EXPECTED = (1024, 1024)


def png_size(path):
    with open(path, "rb") as fh:
        head = fh.read(24)
    if len(head) < 24 or head[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG file")
    width, height = struct.unpack(">II", head[16:24])
    return width, height


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    if not os.path.isfile(src):
        print("entry.png missing beside main.py", file=sys.stderr)
        return 1
    size = os.path.getsize(src)
    if size > MAX_BYTES:
        print(f"entry.png is {size} bytes, over the 1 MiB limit",
              file=sys.stderr)
        return 1
    dims = png_size(src)
    if dims != EXPECTED:
        print(f"entry.png is {dims[0]}x{dims[1]}, expected 1024x1024",
              file=sys.stderr)
        return 1
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(outdir, exist_ok=True)
    dst = os.path.join(outdir, "entry.png")
    shutil.copyfile(src, dst)
    print(f"entry.png -> {dst} ({size} bytes, {dims[0]}x{dims[1]})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
