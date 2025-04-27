#!/usr/bin/env python3
import os
import sys
import shutil

src = sys.argv[1]
dst = sys.argv[2]
max_depth = None

if len(sys.argv) > 4 and sys.argv[3] == "--max_depth":
    max_depth = int(sys.argv[4])

src = os.path.abspath(src)
dst = os.path.abspath(dst)
os.makedirs(dst, exist_ok=True)

for root, _, files in os.walk(src):
    rel = os.path.relpath(root, src)
    parts = rel.split(os.sep) if rel != "." else []
    current_depth = len(parts)

    for name in files:
        full_parts = parts + [name]

        if max_depth is not None and current_depth + 1 > max_depth:
            keep = parts[:max_depth - 1]
            rest = parts[max_depth - 1:]
            path_parts = keep + rest
            sub_path = os.path.join(*path_parts) if path_parts else ""
        else:
            sub_path = os.path.join(*parts) if parts else ""

        outdir = os.path.join(dst, sub_path)
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
