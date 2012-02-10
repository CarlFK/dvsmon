#!/usr/bin/python

COMMANDS.append(
  Command('dvsink-command %s -- ffplay - -f dv -vn -framedrop -threads 1 '
          '-loglevel 0 -flags low_delay -x 400 -y 200'
          % (hostport,)))


