
COMMANDS = [
    'dvswitch',
    'dvsource-firewire -c 0',
    'dvsource-firewire -c 1',
    'ssh slave dvsource-firewire -c 0',
    'ssh slave dvsource-firewire -c 1',
    'dvsource-alsa -s ntsc -r 48000 hw:1',
    'dvsink-files /home/juser/Video/dv/%Y-%m-%d/%H:%M:%S.dv',
    'dvsink-command -- playdv',
    'dvsink-command -- ffplay',
    ]

