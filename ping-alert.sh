#!/bin/bash
while true; do
  date
  ping -q -c 1 -W 5 8.8.8.8 > /dev/null
  if [ $? -eq 0 ]; then
    notify-send "ping-alert" "network available"
    echo "Network available!"
    break
  fi
  sleep 5
done
