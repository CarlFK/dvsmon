#!/usr/bin/python

# pipe doesn't work ...

COMMANDS.append( 
 'dvsink-command -- ffmpeg2theora - -f dv -F 25:5 --speedlevel 0 -v 4 -a 0 -c 1 -H 9600 -o - | oggfwd giss.tv 8001 $STREAMPW /CarlFK.ogg'
 % (hostport,))


