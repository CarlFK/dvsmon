
COMMANDS = [
    Command ('dvswitch', 'Video mixer'),
    Command ('dvsource-firewire', 'Firewire DV camera'),
    Command ('dvsink-files /home/juser/Videos/dv/%Y-%m-%d/%H_%M_%S.dv', 'Record to disk'),
    Command ('ssh cnt1.local dvsource-firewire -c 0 -n /home/juser/Videos/dv/c1/%Y-%m-%d/%H_%M_%S.dv', 'Remote camera 1'),
    Command ('ssh cnt1.local dvsource-firewire -c 0 -n /home/juser/Videos/dv/c2/%Y-%m-%d/%H_%M_%S.dv', 'Remote camera 2')
    ]

