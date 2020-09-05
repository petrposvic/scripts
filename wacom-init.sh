#!/bin/bash

DEVICE="Wacom One by Wacom M Pen stylus"

# Map to top monitor
xsetwacom set "$DEVICE" MapToOutput 1920x1080+0+0

# Map lower pen button to CTRL+Z (undo)
xsetwacom set "$DEVICE" Button 2 "key ctrl z"

# Map higher pen button to middle mouse button
xsetwacom set "$DEVICE" Button 3 2
