#!/bin/bash

SRC="$1"
DST="$2"
DEPTH=""

if [ "$3" = "--max_depth" ]; then
  DEPTH="$4"
elif echo "$3" | grep -q "^--max_depth="; then
  DEPTH=$(echo "$3" | cut -d'=' -f2)
fi

javac CollectorMain.java

if [ $? -eq 0 ]; then
  if [ -n "$DEPTH" ]; then
    java CollectorMain "$SRC" "$DST" "$DEPTH"
  else
    java CollectorMain "$SRC" "$DST"
  fi
else
  exit 1
fi
