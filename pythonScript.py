#!/usr/bin/env python3
import os
import shutil
import sys

src = sys.argv[1]
dst = sys.argv[2]
max_depth = None

if len(sys.argv) > 4 and sys.argv[3] == "--max_depth":
    max_depth = int(sys.argv[4])

src = src.rstrip("/")
dst = dst.rstrip("/")
os.makedirs(dst, exist_ok=True)

for root, _, files in os.walk(src):
    rel = os.path.relpath(root, src)
    parts = rel.split(os.sep) if rel != "." else []
    depth = len(parts) + 1

    for name in files:
        if max_depth is not None and depth > max_depth:
            prefix = parts[:max_depth - 1]
            suffix = parts[max_depth - 1:]
            subdir = os.path.join(*(prefix + suffix)) if prefix or suffix else ""
        else:
            subdir = rel if rel != "." else ""

        outdir = os.path.join(dst, subdir)
        os.makedirs(outdir, exist_ok=True)

        src_path = os.path.join(root, name)
        dst_path = os.path.join(outdir, name)

        if os.path.exists(dst_path):
            base, ext = os.path.splitext(name)
            i = 1
            while True:
                alt_name = f"{base}_{i}{ext}"
                alt_path = os.path.join(outdir, alt_name)
                if not os.path.exists(alt_path):
                    dst_path = alt_path
                    break
                i += 1

        shutil.copy2(src_path, dst_path)
