#!/usr/bin/env python3
"""THE WORLD IN A DAY -- front page for Tuesday 24 November 2026.

The entry image (front-page.jpg, shipped beside this program) is a
newspaper front page generated with Google Gemini (AI Plus) from the
day's reported headlines: Jensen Huang reinstated at Nvidia as the
stock soared 31% in a record tech rebound, Ukraine sinking a Russian
warship off Libya, Mexico defying a US extradition request for cartel
boss "El Chapo Isidro", and oil sliding to $80 on US-Iran talks.

This program is the make.fun entry: standard library only, no network,
fully deterministic. It reads front-page.jpg, sanity-checks that the
file is a whole JPEG inside the competition limits (at most 1 MiB and
at most 1024x1024 pixels, read from the JPEG SOF header), and writes
the bytes unchanged to $MAKEFUN_OUTPUT_DIR/entry.png (default
/output/entry.png). Two runs write byte-identical output.
"""

import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
IMAGE_PATH = os.path.join(HERE, "front-page.jpg")

MAX_BYTES = 1_048_576          # competition cap: 1 MiB
MAX_WIDTH = 1024               # competition cap: 1024 px
MAX_HEIGHT = 1024              # competition cap: 1024 px

JPEG_SOI = b"\xff\xd8"         # start of image
JPEG_EOI = b"\xff\xd9"         # end of image

# SOF (start of frame) markers carry the frame dimensions. SOF0/SOF1/
# SOF2 are the common ones; the full set excludes DHT, JPG and DAC.
SOF_MARKERS = {
    0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
    0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF,
}
# Markers with no length field: TEM, RST0-RST7, SOI, EOI.
STANDALONE_MARKERS = {0x01, 0xD8, 0xD9} | set(range(0xD0, 0xD8))
SOS_MARKER = 0xDA              # start of scan: header segments end here


def jpeg_dimensions(data):
    """Return (width, height) parsed from the JPEG SOF header.

    Walks the marker segments after the SOI marker until a start-of-
    frame segment is found. Raises ValueError on malformed input.
    """
    if not data.startswith(JPEG_SOI):
        raise ValueError("not a JPEG: missing FF D8 start-of-image marker")
    pos = 2
    end = len(data)
    while pos + 1 < end:
        if data[pos] != 0xFF:
            raise ValueError(f"malformed JPEG: expected marker at byte {pos}")
        marker = data[pos + 1]
        if marker in STANDALONE_MARKERS:
            pos += 2
            continue
        if marker == SOS_MARKER:
            break
        if pos + 3 >= end:
            raise ValueError("malformed JPEG: truncated segment header")
        seg_len = struct.unpack(">H", data[pos + 2:pos + 4])[0]
        if seg_len < 2:
            raise ValueError("malformed JPEG: bad segment length")
        if marker in SOF_MARKERS:
            if pos + 8 >= end:
                raise ValueError("malformed JPEG: truncated SOF segment")
            height = struct.unpack(">H", data[pos + 5:pos + 7])[0]
            width = struct.unpack(">H", data[pos + 7:pos + 9])[0]
            return width, height
        pos += 2 + seg_len
    raise ValueError("no start-of-frame segment found before scan data")


def check_image(data):
    """Validate the shipped image against the competition's gate rules.

    Returns (width, height). Raises ValueError with a precise reason
    when the image is not a whole JPEG inside the size/pixel limits.
    """
    if len(data) > MAX_BYTES:
        raise ValueError(f"image is {len(data)} bytes, over the {MAX_BYTES} cap")
    if not data.startswith(JPEG_SOI):
        raise ValueError("image does not start with the JPEG SOI marker")
    if not data.endswith(JPEG_EOI):
        raise ValueError("image does not end with the JPEG EOI marker")
    width, height = jpeg_dimensions(data)
    if width > MAX_WIDTH or height > MAX_HEIGHT:
        raise ValueError(
            f"image is {width}x{height}, over the {MAX_WIDTH}x{MAX_HEIGHT} cap"
        )
    return width, height


def main():
    with open(IMAGE_PATH, "rb") as fh:
        data = fh.read()
    width, height = check_image(data)

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.png")
    with open(out_path, "wb") as fh:
        fh.write(data)

    print(f"entry.png written: {len(data)} bytes, {width}x{height} JPEG")
    return 0


if __name__ == "__main__":
    sys.exit(main())
