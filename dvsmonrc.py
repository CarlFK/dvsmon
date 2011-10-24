
COMMANDS = [
    'dvswitch',
    'dvsource-firewire',
    'dvsink-files /home/juser/Videos/dv/%Y-%m-%d/%H_%M_%S.dv',
    'ssh cnt1.local dvsource-firewire -c 0 -n /home/juser/Videos/dv/c1/%Y-%m-%d/%H_%M_%S.dv',
    'ssh cnt1.local dvsource-firewire -c 0 -n /home/juser/Videos/dv/c2/%Y-%m-%d/%H_%M_%S.dv',
    ]

