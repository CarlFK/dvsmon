#!/usr/bin/python

COMMANDS.append( 
  'dvsink-command -- ffplay - -f dv -vn -framedrop -threads 1 '
  '-loglevel 0 -flags low_delay -x 400 -y 200 %s' 
    % (hostport,))


