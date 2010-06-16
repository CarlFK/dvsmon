#!/usr/bin/python

# find a place to save files
# look for ~/Videos, then /media/disk, then /media/*

import os
import socket

# make a list of dirs to search - 
# use any that have a dv or veyepar dir
# else find the 'best' one.
# home dir
dirs  = [os.path.expanduser('~/Videos/veyepar')]
# anyting mounted under /media with a Videos/veyepar dir
dirs += ["/media/%s/Videos/veyepar"%dir for dir in os.listdir('/media') if dir[0]!='.' ]
# can't find a veyepar dir. now start looking for anything reasonable. 
# someday maybe search for something with the most free space.
dirs += ["/media/%s/Videos"%dir for dir in os.listdir('/media') if dir[0]!='.' ]
dirs += [os.path.expanduser('~/Videos')]
# rom excludes cdrom cdrom-1 or any other rom.
dirs += ["/media/%s"%dir 
    for dir in os.listdir('/media') \
        if (dir[0]!='.' 
            and 'rom' not in dir
            and 'floppy' not in dir) ]
# if we get here, I hope it isn't the live CD.
dirs += [os.path.expanduser('~')]

print "dirs to check:", dirs

vid_dirs=[]
for vid_dir in dirs:
    print "checking", vid_dir
    if os.path.exists(vid_dir):
        print "found, checking for write perms..." 
        w_perm = os.access(vid_dir, os.W_OK)
        print 'os.access("%s", os.W_OK): %s'%( vid_dir, w_perm )
        if w_perm:
            s=os.statvfs(vid_dir)
            print 'block size: %s' % s.f_bsize
            print 'free blocks: %s' % s.f_bavail
            gigfree=s.f_bsize * s.f_bavail / 1024.0**3
            minutes = gigfree/.23
            print 'free space: %s gig' % round(gigfree,1)
            print 'room for: %s min' % round(minutes,1)
            if minutes>5:
                vid_dirs.append(vid_dir)
            else:
                print "%s minutes is not enough." % (minutes)


hostname=socket.gethostname()

COMMANDS = [
    'dvswitch',
    'dvsource-alsa -s ntsc -r 48000 hw:1',
    'dvsource-firewire',
    'dvsource-firewire -c 1',
    ]
for vid_dir in vid_dirs:
    COMMANDS.append('dvsink-files ' + os.path.join( vid_dir, 'dv',
        hostname,'%Y-%m-%d','%H:%M:%S.dv' ))

# find test files
if os.path.exists('/usr/share/dvsmon/dv/test-1.dv'):
    for i in '123': 
        COMMANDS += [ 'dvsource-file -l /usr/share/dvsmon/dv/test-%s.dv'%i ]
elif os.path.exists('app_data/dv/test-1.dv'):
    for i in '123': 
        COMMANDS += [ 'dvsource-file -l app_data/dv/test-%s.dv'%i ]



# ffmpeg -f video4linux2 -s 1024x768 -i /dev/video0 -target ntsc-dv -y - | dvsource-file /dev/stdin
# 'dvsink-command -- ffmpeg2theora - -f dv -F 25:5 -v 2 -a 1 -c 1 -H 11025 -o - | oggfwd giss.tv 8001 my_pw /CarlFK.ogg"',

##==============================================================================
import optparse

import wx
import wx.lib.sized_controls as sc

def main():
    app = wx.PySimpleApp()
    
    size=wx.GetDisplaySize()
    print size
        
    frame = sc.SizedFrame(None, title='dvs-mon',  pos=(1,1), size=(450, size[1]))
    
    panel = frame.GetContentsPane()

    timer = wx.Timer(panel)
    timer.Start(1000)

    timerCallbacks = []
    
    for cmd in COMMANDS:
        cr = CommandRunner(cmd)
        cr.addWidgets(panel, frame)

    def OnTimer(evt):
        for cb in CommandRunner.timerCallbacks:
            cb(evt)

    panel.Bind(wx.EVT_TIMER, OnTimer)

    frame.Show()
    # SetSizeHints(minW, minH, maxW, maxH)

    app.MainLoop()

class CommandRunner:
    timerCallbacks = []
    
    def __init__(self, cmd):
        self.cmd = cmd
        self.process = None
        
    def addWidgets(self, parent, topwindow):
        panel = sc.SizedPanel(parent)
        panel.SetSizerType('horizontal')
        panel.SetSizerProps(expand=True)
        panel.Bind(wx.EVT_END_PROCESS, self.OnProcessEnded)
        self.panel = panel
        self.pid=None

        txt1 = wx.TextCtrl(panel, value=self.cmd, style=wx.TE_READONLY)
        # txt1 = wx.TextCtrl(panel, value=self.cmd)
        txt1.SetForegroundColour(wx.BLUE)
        txt1.SetSizerProps(proportion=40, expand=True)
        self.txt1=txt1

        btn1 = wx.Button(panel, label='Run')
        btn1.Bind(wx.EVT_BUTTON, self.OnRunClicked)
        btn1.SetSizerProps(proportion=5, expand=True)

        btn2 = wx.Button(panel, label='Kill')
        btn2.Bind(wx.EVT_BUTTON, self.OnKillClicked)
        btn2.SetSizerProps(proportion=5, expand=True)
        
        btn3 = wx.Button(panel, label='X')
        btn3.Bind(wx.EVT_BUTTON, self.OnXClicked)
        btn3.SetSizerProps(proportion=3, expand=True)
        
        panel2 = sc.SizedPanel(parent)
        panel2.SetSizerType('vertical')
        panel2.SetSizerProps(expand=True, proportion=2)
        self.panel2 = panel2

        txt2 = wx.TextCtrl(panel2, style=wx.TE_READONLY|wx.TE_MULTILINE)
        txt2.SetSizerProps(proportion=1, expand=True)
        self.stdout = txt2

        txt3 = wx.TextCtrl(panel2, style=wx.TE_READONLY|wx.TE_MULTILINE)
        txt3.SetSizerProps(proportion=1, expand=True)
        txt3.SetForegroundColour(wx.RED)
        self.stderr = txt3

        # Return the timer callback:
        self.timerCallbacks.append(self.OnTimer)
        
    def OnRunClicked(self, event):
        if self.pid is None:
            self.txt1.SetForegroundColour(wx.GREEN)
            self.process = wx.Process(self.panel)
            self.process.Redirect()
            self.pid = wx.Execute(self.cmd, wx.EXEC_ASYNC, self.process)
            print 'Executed: ' + self.cmd
            
    def OnKillClicked(self, event):
        if self.pid:
            print 'Trying to kill process %d: %s' % (self.pid, self.cmd)
            wx.Process.Kill(self.pid)
            self.pid = None
            self.txt1.SetForegroundColour(wx.BLUE)
        
    def OnXClicked(self, event):
        # remove this command to make room for the stuff we care about
        if self.pid is None:
            parent=self.panel.GetTopLevelParent() # Parent
            self.panel.Destroy() 
            self.stdout.Destroy() 
            self.stderr.Destroy() 
            self.panel2.Destroy() 
            parent.SendSizeEvent()
            
    def OnTimer(self, event):
        if self.process is not None:
            stream = self.process.GetInputStream()
            if stream.CanRead():
                self.stdout.AppendText("\n"+stream.read().strip())

            stream = self.process.GetErrorStream()
            if stream.CanRead():
                self.stderr.AppendText("\n"+stream.read().strip())

    def OnProcessEnded(self, event):
        if self.pid:
            self.txt1.SetForegroundColour(wx.RED)
        stream = self.process.GetInputStream()

        if stream.CanRead():
            self.stdout.AppendText(stream.read())

        self.process.Destroy()
        self.process = None

        print 'Process %s terminated: %s' % (self.pid, self.cmd)
        self.pid=None

def parse_args():
    parser = optparse.OptionParser()
    parser.add_option('-v', '--verbose', action="store_true" )
    parser.add_option('-c', '--commands', 
      help="command file" )

    options, args = parser.parse_args()
    return options, args

if __name__ == '__main__':
    options, args = parse_args()
    if options.commands:
        settings = {'COMMANDS':COMMANDS}
        execfile(options.commands, settings)
        COMMANDS = settings['COMMANDS']
    main()
