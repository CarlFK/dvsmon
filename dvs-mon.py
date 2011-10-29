#!/usr/bin/python

import argparse
import time

import wx
import wx.lib.sized_controls as sc

class CommandRunner(object):

    """
    gievn a shell command
    adds a panel to the main window with the following:
    display the command 
    buttons to run/kill the command
    X to remove the panel, but only if the command is not running
    multiline text areas for stdout, stderr
    """

    process = None
    detail = False
    keepalive = False
    
    def __init__(self, pain, i, cmd, args):

        self.cmd = cmd
        if args.keepalive:
            self.keepalive = int(args.keepalive)
            # extra delay to spread out startup
            self.deadtime = int(args.keepalive) * (i+1)/2
        else:
            self.keepalive = False
        
        # outer panel to hold the 3 parts:
        #  cmd+buttons, stdout, stderr
        panel_cr = sc.SizedPanel(pain)
        panel_cr.SetSizerType('vertical')
        panel_cr.SetSizerProps(proportion=1, expand=True)
        panel_cr.Bind(wx.EVT_END_PROCESS, self.ProcessEnded)
        self.panel_cr = panel_cr

        # cmd+buttons
        panel_cmd = sc.SizedPanel(panel_cr)
        panel_cmd.SetSizerType('horizontal')
        panel_cmd.SetSizerProps(expand=True)

        self.txt_cmd = wx.TextCtrl(
                panel_cmd, value=self.cmd, style=wx.TE_READONLY)
        self.txt_cmd.SetSizerProps(proportion=1, expand=True)
        self.txt_cmd.SetForegroundColour(wx.BLUE)

        btn1 = wx.Button(panel_cmd, label='Run', size=(45, -1))
        btn1.Bind(wx.EVT_BUTTON, self.RunCmd)

        btn2 = wx.Button(panel_cmd, label='Kill', size=(45,-1))
        btn2.Bind(wx.EVT_BUTTON, self.Kill)
        
        btn3 = wx.Button(panel_cmd, label='Detail', size=(50,-1))
        btn3.Bind(wx.EVT_BUTTON, self.Detail)
        
        btn4 = wx.Button(panel_cmd, label='X', size=(25,-1))
        btn4.Bind(wx.EVT_BUTTON, self.RemovePanel)
        
        # sdtout
        stdout = wx.TextCtrl( 
                panel_cr, style=wx.TE_READONLY|wx.TE_MULTILINE)
        stdout.SetSizerProps(proportion=1, expand=True)
        self.stdout = stdout

        # stderr
        stderr = wx.TextCtrl( 
                panel_cr, style=wx.TE_READONLY|wx.TE_MULTILINE)
        stderr.SetSizerProps(proportion=1, expand=True)
        stderr.SetForegroundColour(wx.RED)
        self.stderr = stderr

        panel_cr.Bind(wx.EVT_TIMER, self.OnTimer)
        self.timer = wx.Timer( panel_cr )
        self.timer.Start(100)

        
    def AppendLine(self, ctrl, line):
        ctrl.AppendText("\n"+line)

    def MarkOuts(self, line):
        self.AppendLine(self.stdout,line)
        self.AppendLine(self.stderr,line)

    def RunCmd(self, event=None):
        if self.process is None:
            self.MarkOuts("Starting...")
            self.txt_cmd.SetForegroundColour(wx.GREEN)
            self.process = wx.Process(self.panel_cr)
            self.process.Redirect()
            self.pid = wx.Execute(
                    self.cmd, wx.EXEC_ASYNC, self.process)
            print 'Executed:  %s' % (self.cmd)
            
    def Kill(self, event):
        if self.process is not None:
            self.MarkOuts("Killing...")
            print 'Killing: %s' % (self.cmd)
            wx.Process.Kill(self.pid)
            self.pid = None
            self.txt_cmd.SetForegroundColour(wx.BLUE)
            self.keepalive = 0
           
    def ShowIO(self):
        if self.process is not None:

            def one(stream,ctrl):
              while stream.CanRead():
                line = stream.read()
                line = line.strip()
                self.AppendLine(ctrl,line)

            one(self.process.GetInputStream(), self.stdout)
            one(self.process.GetErrorStream(), self.stderr)
 
    def KeepAlive(self):
        if self.deadtime:
            self.deadtime-=1
            print self.deadtime
        else:
            self.RunCmd()

    def OnTimer(self,event):
        self.ShowIO()
        if self.keepalive:
            self.KeepAlive()

    def ProcessEnded(self, event):
        if self.process is not None:
            self.txt_cmd.SetForegroundColour(wx.RED)
            self.ShowIO()
            self.MarkOuts("DIED!")

        self.process.Destroy()
        self.process = None

        print 'Process %s terminated: %s' % (self.pid, self.cmd)
        self.pid=None
        self.deadtime = self.keepalive


    def Detail(self, event=None):
        # show/hide stdout/err

        if self.detail: 
            # squish
            self.panel_cr.SetSizerProps(proportion=1, expand=True)
        else: 
            # restore to normal size
            self.panel_cr.SetSizerProps(proportion=10, expand=True)

        parent=self.panel_cr.GetTopLevelParent() 
        parent.SendSizeEvent()
        
        # flip state for next time
        self.detail = not self.detail
        
    def RemovePanel(self, event):
        if self.process is None:
            parent=self.panel_cr.GetTopLevelParent() 
            self.panel_cr.Destroy() 
            parent.SendSizeEvent()

def mk_commands(args):

    host = "--host %s" % args.host if args.host else ''
    port = "--port %s" % args.port if args.port else ''
    hostport = ' '.join([host,port])

    # COMMANDS is caps cuz it is global
    # cuz I am not sure how to api the plugin like thing
    # where I use execfile() - it works.

    if args.commands:
        COMMANDS = [ ]
        for cmd_file in args.commands:
            execfile(cmd_file, locals())
    else:
        # for testing.
        COMMANDS=[ 
            'ping -i .3 127.0.0.1',
            'ping -i 1 127.0.0.1',
            'ping localhost',
            'ping -c 5 localhost',
        ]

    # strip trailing spaces which get passed as a parameter.
    commands = [cmd.strip() for cmd in COMMANDS]

    return commands

def parse_args():
    parser = argparse.ArgumentParser(description='DVswitch manager.')
    parser.add_argument('--host')
    parser.add_argument('-p', '--port')
    parser.add_argument('-k', '--keepalive', )
    parser.add_argument('-c', '--commands', nargs="*",
      help="command file" )
    parser.add_argument('-v', '--verbose', action="store_true" )

    args = parser.parse_args()
    return args

def main():
    
    args = parse_args()
    commands=mk_commands(args)
    
    app = wx.PySimpleApp()
    
    size=wx.GetDisplaySize()
    frame = sc.SizedFrame(
            None, title='dvs-mon',  pos=(1,1), size=(450, size[1]-100))
    pain = frame.GetContentsPane()

    crs = []
    for i, cmd in enumerate(commands):
        cr = CommandRunner( pain, i, cmd, args )
        crs.append(cr)

    cr.Detail(cr)
    frame.Show()

    app.MainLoop()

if __name__ == '__main__':
    main()
