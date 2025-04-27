#!/bin/bash

SRC="$1"
DST="$2"
DEPTH=""

if [ "$3" = "--max_depth" ]; then
  DEPTH="$4"
elif echo "$3" | grep -q "^--max_depth="; then
  DEPTH=$(echo "$3" | cut -d'=' -f2)
fi

javac CollectorMain.java >/dev/null 2>&1

if [ -n "$DEPTH" ]; then
  java CollectorMain "$SRC" "$DST" "$DEPTH" >/dev/null 2>&1
else
  java CollectorMain "$SRC" "$DST" >/dev/null 2>&1
fi
