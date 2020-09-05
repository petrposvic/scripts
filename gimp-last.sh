#!/bin/bash
set -euo pipefail

DIR="./"
if [ $# -eq 1 ]; then
  DIR=$1
fi

if [ $# -gt 1 ]; then
  echo "Usage: $0 [DIR]"
  exit 1
fi

LAST_FILENAME=`find $DIR -maxdepth 1 -type f -name "*.jpg" -printf '%T@ %p\n' | sort -k1,1nr | head -1 | cut -d' ' -f2-`
echo "Opening file '$LAST_FILENAME'"
gimp "$LAST_FILENAME"
