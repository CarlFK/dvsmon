#!/usr/bin/python

# find a place to save files
# look for ~/Videos, then /media/disk, then /media/*

COMMANDS = [
    'dvswitch',
    'dvsource-alsa -s ntsc -r 48000 hw:1',
    'dvsource-firewire',
    'dvsource-firewire -c 1',
    'dvsource-file -l /usr/share/dvsmon/dv/test-1.dv',
    'dvsource-file -l /usr/share/dvsmon/dv/test-2.dv',
    'dvsink-files Videos/dv/%Y-%m-%d/%H:%M:%S.dv',
    'dvsink-files /media/disk/Videos/dv/%Y-%m-%d/%H:%M:%S.dv',
    ]

# ffmpeg -f video4linux2 -s 1024x768 -i /dev/video0 -target ntsc-dv -y - | dvsource-file /dev/stdin
# 'dvsink-command -- ffmpeg2theora - -f dv -F 25:5 -v 2 -a 1 -c 1 -H 11025 -o - | oggfwd giss.tv 8001 my_pw /CarlFK.ogg"',

##==============================================================================
import wx
import wx.lib.sized_controls as sc

def main():
    app = wx.PySimpleApp()
    
    size=wx.GetDisplaySize()
    print size
        
    frame = sc.SizedFrame(None, title='dvs-mon',  pos=(1,1), size=(800, size[1]))
    
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
        self.txt1.SetForegroundColour(wx.RED)
        stream = self.process.GetInputStream()

        if stream.CanRead():
            self.stdout.AppendText(stream.read())

        self.process.Destroy()
        self.process = None

        print 'Process %s terminated: %s' % (self.pid, self.cmd)
        self.pid=None

            
if __name__ == '__main__':
    main()
