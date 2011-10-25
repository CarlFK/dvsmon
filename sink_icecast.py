#!/usr/bin/python

COMMANDS.append( 'ffmpeg -f video4linux2 -s 1024x768 -i /dev/video0 -target ntsc-dv -y - | dvsource-file /dev/stdin %s' % (hostport,))


