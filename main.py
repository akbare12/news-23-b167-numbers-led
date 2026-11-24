#!/usr/bin/env python3
"""news-23 b167 numbers-led entry generator (stdlib only, no PIL).

Validates the bundled entry.png and writes a byte-identical copy to
os.path.join(os.environ.get("MAKEFUN_OUTPUT_DIR", "out"), "entry.png").
"""
import hashlib
import os
import struct
import sys
import zlib

EXPECTED_SHA256 = "78140e6077c352c10b89503d37d8dce862345d04bb9858f8e0023fd4b3af7719"
EXPECTED_SIZE = 142315

SOURCE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")


def fail(msg):
    print("ERROR: " + msg, file=sys.stderr)
    sys.exit(1)


def read_png(path):
    with open(path, "rb") as fh:
        data = fh.read()
    if len(data) < 8 or data[:8] != b"\x89PNG\r\n\x1a\n":
        fail("bad PNG signature")
    if len(data) < 33:
        fail("PNG too small")
    length, ctype = struct.unpack(">I4s", data[8:16])
    if ctype != b"IHDR" or length != 13:
        fail("first chunk must be a 13-byte IHDR")
    w, h, depth, ctype2, comp, filt, inter = struct.unpack(">IIBBBBB", data[16:29])
    if (w, h) != (1024, 1024):
        fail("entry.png must be 1024x1024, got %dx%d" % (w, h))
    if depth != 8 or ctype2 not in (2, 6):
        fail("unsupported bit depth / colour type")
    if comp != 0 or filt != 0 or inter != 0:
        fail("unsupported compression/filter/interlace")
    crc_stored = struct.unpack(">I", data[29:33])[0]
    if zlib.crc32(data[12:29]) & 0xFFFFFFFF != crc_stored:
        fail("IHDR CRC mismatch")
    # Walk chunks: every CRC must match, every IDAT non-empty, IEND last.
    pos = 8
    idat_total = 0
    saw_iend = False
    while pos < len(data):
        if pos + 8 > len(data):
            fail("truncated chunk header")
        clen, ctype = struct.unpack(">I4s", data[pos:pos + 8])
        end = pos + 8 + clen + 4
        if end > len(data):
            fail("truncated chunk %r" % ctype)
        crc_stored = struct.unpack(">I", data[pos + 8 + clen:end])[0]
        if zlib.crc32(data[pos + 4:pos + 8 + clen]) & 0xFFFFFFFF != crc_stored:
            fail("CRC mismatch in chunk %r" % ctype)
        if ctype == b"IDAT":
            if clen == 0:
                fail("empty IDAT chunk")
            idat_total += clen
        if ctype == b"IEND":
            if clen != 0:
                fail("IEND must be empty")
            if end != len(data):
                fail("trailing data after IEND")
            saw_iend = True
            break
        pos = end
    if not saw_iend:
        fail("missing IEND chunk")
    if idat_total < 1000:
        fail("IDAT payload too small")
    if len(data) < 10000:
        fail("entry.png too small")
    if len(data) > 1024 * 1024:
        fail("entry.png exceeds 1 MiB")
    return data


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    if not out_dir:
        fail("MAKEFUN_OUTPUT_DIR is empty")
    out_dir_abs = os.path.abspath(out_dir)
    repo = os.path.dirname(os.path.abspath(__file__))
    if out_dir_abs == repo or out_dir_abs.startswith(repo + os.sep):
        fail("MAKEFUN_OUTPUT_DIR must be outside the repo")
    if os.path.exists(out_dir_abs) and not os.path.isdir(out_dir_abs):
        fail("MAKEFUN_OUTPUT_DIR is a file, not a directory")
    data = read_png(SOURCE)
    if hashlib.sha256(data).hexdigest() != EXPECTED_SHA256:
        fail("sha256 mismatch")
    if len(data) != EXPECTED_SIZE:
        fail("size mismatch")
    out_path = os.path.join(out_dir_abs, "entry.png")
    if os.path.abspath(out_path) == os.path.abspath(SOURCE):
        fail("output would overwrite the source")
    os.makedirs(out_dir_abs, exist_ok=True)
    with open(out_path, "wb") as fh:
        fh.write(data)
    with open(out_path, "rb") as fh:
        back = fh.read()
    if back != data:
        fail("output is not byte-identical to the source")
    print("wrote %s (%d bytes, sha256 %s)" % (out_path, len(data), EXPECTED_SHA256))


if __name__ == "__main__":
    main()
