#!/bin/bash

src="$1"
dst="$2"
limit=""

[[ "$3" == "--max_depth" ]] && limit="$4"

src="${src%/}"
dst="${dst%/}"
mkdir -p "$dst"

find "$src" -type f | while read -r path; do
    relative="${path#$src/}"

    IFS='/' read -r -a segments <<< "$relative"
    depth="${#segments[@]}"

    if [[ -n "$limit" && "$depth" -gt "$limit" ]]; then
        trimmed=""
        for ((i = 0; i < limit; i++)); do
            trimmed+="${segments[i]}/"
        done
        trimmed+="${segments[limit-1]}"
        target_path="$dst/$trimmed"
    else
        target_path="$dst/$relative"
    fi

    folder=$(dirname "$target_path")
    name=$(basename "$target_path")
    mkdir -p "$folder"

    final="$folder/$name"
    if [[ -e "$final" ]]; then
        base="${name%.*}"
        ext="${name##*.}"
        [[ "$base" == "$ext" ]] && ext=""
        count=1
        while [[ -e "$folder/${base}_$count.${ext}" ]]; do
            ((count++))
        done
        final="$folder/${base}_$count.${ext}"
    fi

    cp "$path" "$final"
done
