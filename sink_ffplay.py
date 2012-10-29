#!/usr/bin/python

"""
 -f dv - forrce DV format
  -vn - Disable video.
  -fast Non-spec-compliant optimizations.
  -autoexit Exit when video is done playing.

   cat test.wav | ffmpeg -i pipe:

"""

COMMANDS.append(
  Command('dvsink-command %s -- ffplay - -f dv -vn -framedrop -threads 1 '
          '-loglevel quiet -flags low_delay -x 400 -y 200'
          % (hostport,)))


