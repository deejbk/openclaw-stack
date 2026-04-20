#!/bin/bash

QUERY="$1"
KB_DIR="$HOME/openclaw/knowledge"

if [ -z "$QUERY" ]; then
  echo "Usage: ./retrieve.sh <query>"
  exit 1
fi

grep -i -r --color=always "$QUERY" "$KB_DIR"
