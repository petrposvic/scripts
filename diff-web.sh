#!/bin/bash

name=$1
addr=$2

if [ -f "diff-web/$name" ]; then
  wget --quiet -O "diff-web/$name.new" -P diff-web "$addr"
  diff -c "diff-web/$name" "diff-web/$name.new" >> "diff-web/$name.change"
  if [ $? -ne 0 ]; then
    # TODO Notify
    echo "Some change on $name ($addr)"
    rm "diff-web/$name"
    rm "diff-web/$name.new"
  fi
else
  echo "First run on $name ($addr)"
  wget --quiet -O "diff-web/$name" -P diff-web "$addr"
fi

