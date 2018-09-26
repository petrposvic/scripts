#!/bin/bash

# Move mouse to specified position and click
#
# Needs xdotool utility
#   sudo apt install xdotool

# xdotool mousemove 1250 750 click 1 mousemove restore
/usr/bin/xdotool mousemove 1250 750 sleep 0.2 click 1
