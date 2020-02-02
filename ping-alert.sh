#!/bin/bash

systemctl --user --quiet is-active dunst.service
if [ $? -ne 0 ]; then
  echo "dunst service is not running. Run it via:"
  echo "  systemctl --user start dunst.service"
  echo "If you don't use display manager you should"
  echo "export DISPLAY via:"
  echo "  systemctl --user import-environment DISPLAY"
  echo "command. You can save it in ~/.xinitrc."
  exit 1
fi

while true; do
  date
  ping -q -c 1 -W 5 8.8.8.8 > /dev/null
  if [ $? -eq 0 ]; then
    echo "Network available!"
    notify-send "ping-alert" "network available"
    break
  fi
  sleep 5
done
