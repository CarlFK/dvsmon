#!/bin/bash
# Generates an ffmpeg command line for capturing a given X11 window.
# Usage: $0 [optional output file name]
# It will prompt you to click on the window you want to capture.
# Output is simply echoed, for use in copy/pasting (adjusting/adding
# parameters as needed).
# Tip: the command uses screen coordinates, so do not resize or move
# the target window once capturing as begun.
echo "Click the window to capture..."

tmpfile=/tmp/screengrab.tmp.$$
trap 'touch $tmpfile; rm -f $tmpfile' 0

xwininfo > $tmpfile 2>/dev/null
left=$(grep 'Absolute upper-left X:' $tmpfile | awk '{print $4}');
top=$(grep 'Absolute upper-left Y:' $tmpfile | awk '{print $4}');
width=$(grep 'Width:' $tmpfile | awk '{print $2}');
height=$(grep 'Height:' $tmpfile | awk '{print $2}');
geom="-geometry ${width}x${height}+${left}+${top}"
echo "Geometry: ${geom}"
size="${width}x${height}"
pos="${left},${top}"
echo "pos=$pos size=$size"

out=${1-screengrab.dv}
#test -f $out && rm $out

ffmpeg -f x11grab \
    -s ${size} \
    -i ${DISPLAY-0:0}+${pos} \
    -acodec pcm_s16le \
    -sameq \
    -target ntsc-dv \
     - | dvsource-file /dev/stdin 

