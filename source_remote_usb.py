#!/usr/bin/python

import os

grab = os.environ['DVS_GRAB']

COMMANDS.append(
 Command('trap "ssh {} killall gst-launch-1.0" TERM; ssh {} dvsource-v4l2-other -d /dev/video0 -c="image/jpeg,width=1280,height=720" -s pal -a 16:9'.format(grab, grab))
)

"""
# magic woo try and fiure it out hope it works it never does.
import socket

hostname=socket.gethostname()
# master = "--host %s.local" % (hostname)
master = "--host %s" % (hostname)
port = "--port %s" % args.port if args.port else ''
hostport = ' '.join([master,port])

slave = 'juser@10.0.0.2'
# slave = 'juser@kasp'

COMMANDS.append(
 Command('ssh %s dvsource-firewire -c 0 %s' % (slave, hostport,))
)
"""

