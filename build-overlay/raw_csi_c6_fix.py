#!/usr/bin/env python3
"""Targeted audited source fix applied only AFTER Stage 5 SHA-256 verification.

A non-trivial C++ struct with default member initializers must not be cleared
using memset under ESP-IDF's -Werror=class-memaccess. Value initialization also
restores the intended RSSI sentinel (-127) and clears all CSI bytes.
"""
from pathlib import Path
p = Path("src/firmware/main/raw_csi.cpp")
src = p.read_text(encoding="utf-8")
old = "    memset(&s_latest,0,sizeof(s_latest));"
new = "    s_latest = RawCsiSnapshot{};"
if src.count(old) != 1:
    raise SystemExit("FAIL: expected exactly one original non-trivial memset; archive or patch changed")
p.write_text(src.replace(old, new), encoding="utf-8")
print("Stage 5 correction: RawCsiSnapshot value initialized; RSSI sentinel retained.")
