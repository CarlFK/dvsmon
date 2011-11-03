#!/usr/bin/python

import socket

hostname=socket.gethostname()
# master = "--host %s.local" % (hostname)
master = "--host %s" % (hostname)
port = "--port %s" % args.port if args.port else ''
hostport = ' '.join([master,port])

# slave = 'juser@10.0.0.2'
slave = 'juser@kasp'

COMMANDS.append(
 'ssh %s dvsource-firewire -c 0 %s' % (slave, hostport,),
)


