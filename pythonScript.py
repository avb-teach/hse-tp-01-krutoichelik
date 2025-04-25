#!/usr/bin/env python3
import os
import shutil
import sys

src = sys.argv[1]
dst = sys.argv[2]
max_depth = None

if len(sys.argv) >= 5 and sys.argv[3] == "--max_depth":
    max_depth = int(sys.argv[4])

src = src.rstrip("/")
dst = dst.rstrip("/")
os.makedirs(dst, exist_ok=True)

for root, _, files in os.walk(src):
    rel = os.path.relpath(root, src)
    parts = [] if rel == "." else rel.split(os.sep)
    depth = len(parts) + 1

    for name in files:
        if max_depth is not None and depth > max_depth:
            trimmed_parts = parts[:max_depth - 1] + [parts[max_depth - 1]]
            subdir = os.path.join(*trimmed_parts) if trimmed_parts else ""
        else:
            subdir = rel if rel != "." else ""

        outdir = os.path.join(dst, subdir)
        os.makedirs(outdir, exist_ok=True)

        src_path = os.path.join(root, name)
        dst_path = os.path.join(outdir, name)

        if os.path.exists(dst_path):
            base, ext = os.path.splitext(name)
            i = 1
            while os.path.exists(os.path.join(outdir, f"{base}_{i}{ext}")):
                i += 1
            dst_path = os.path.join(outdir, f"{base}_{i}{ext}")

        shutil.copy2(src_path, dst_path)
