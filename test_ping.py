#!/usr/bin/python

COMMANDS+=[
    Command('ping -i .3 127.0.0.1'),
    # 'ping -i 1 127.0.0.1',
    # 'ping localhost',
    Command('ping -c 5 localhost'),
]



