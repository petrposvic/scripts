#!/bin/bash

if [ $# -ne 1 ]; then
  echo "Usage: $0 command"
  exit 1
fi

a=`exec $1`
echo "Command \"$1\" has been executed. Do changes and press ENTER."
read input
b=`exec $1`

vimdiff  <(echo "$a" ) <(echo "$b")
