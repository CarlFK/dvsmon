"""Process which doesn't die on SIGTERM."""

import time
import signal
import sys

def handler(signum, frame):
  print "Signal %i received in %s" % (signum, frame)
  sys.stdout.flush()

signal.signal(signal.SIGINT, handler)
signal.signal(signal.SIGTERM, handler)

while True:
  time.sleep(1)
