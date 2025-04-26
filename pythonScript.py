#!/usr/bin/env python3
import os
import shutil
import sys

src = sys.argv[1]
dst = sys.argv[2]
max_depth = None

if len(sys.argv) > 4 and sys.argv[3] == "--max_depth":
    max_depth = int(sys.argv[4])

src = os.path.abspath(src)
dst = os.path.abspath(dst)

for root, _, files in os.walk(src):
    rel = os.path.relpath(root, src)
    parts = [] if rel == "." else rel.split(os.sep)

    for name in files:
        file_parts = parts + [name]
        file_depth = len(file_parts)

        if max_depth is not None and file_depth > max_depth:
            keep_parts = file_parts[:max_depth]
            sub_path = os.path.join(*keep_parts[:-1])
            filename = keep_parts[-1]
        else:
            sub_path = os.path.join(*parts) if parts else ""
            filename = name

        outdir = os.path.join(dst, sub_path)
        os.makedirs(outdir, exist_ok=True)

        dst_path = os.path.join(outdir, filename)
        src_path = os.path.join(root, name)

        if os.path.exists(dst_path):
            base, ext = os.path.splitext(filename)
            i = 1
            while True:
                alt_name = f"{base}_{i}{ext}"
                alt_path = os.path.join(outdir, alt_name)
                if not os.path.exists(alt_path):
                    dst_path = alt_path
                    break
                i += 1

        shutil.copy2(src_path, dst_path)
