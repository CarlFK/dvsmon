#!/usr/bin/python

import argparse

import wx
import wx.lib.sized_controls as sc

class CommandRunner(object):

    """
    gievn a shell command
    adds a panel to the main window with the following:
    display the command 
    buttons to run/kill the command
    X to remove the pannen, but only if the command is not running
    multiline text areas for stdout, stderr
    """

    timerCallbacks = []
    pid=None
    
    def __init__(self, cmd, parent):

        self.cmd = cmd
        self.process = None
        
        # outer panel to hold the 3 parts:
        #  cmd+ctrls, stdout, stderr
        self.panel_out = sc.SizedPanel(parent)
        self.panel_out.SetSizerType('vertical')
        self.panel_out.SetSizerProps(expand=True)

        # self.panel = sc.SizedPanel(parent)
        self.panel = sc.SizedPanel(self.panel_out)
        self.panel.SetSizerType('horizontal')
        self.panel.SetSizerProps(expand=True)
        self.panel.Bind(wx.EVT_END_PROCESS, self.ProcessEnded)

        self.txt_cmd = wx.TextCtrl(self.panel, value=self.cmd, style=wx.TE_READONLY)
        self.txt_cmd.SetSizerProps(proportion=40, expand=True)
        self.txt_cmd.SetForegroundColour(wx.BLUE)

        btn1 = wx.Button(self.panel, label='Run', size=(45, -1))
        btn1.Bind(wx.EVT_BUTTON, self.RunCmd)

        btn2 = wx.Button(self.panel, label='Kill', size=(45,-1))
        btn2.Bind(wx.EVT_BUTTON, self.Kill)
        
        btn3 = wx.Button(self.panel, label='X', size=(25,-1))
        btn3.Bind(wx.EVT_BUTTON, self.RemovePanel)
        
        # self.panel2 = sc.SizedPanel(self.panel)
        # self.panel2 = sc.SizedPanel(parent)
        # self.panel2.SetSizerType('vertical')
        # self.panel2.SetSizerProps(expand=True, proportion=2)
        # self.stdout = wx.TextCtrl( self.panel2, style=wx.TE_READONLY|wx.TE_MULTILINE)

        self.stdout = wx.TextCtrl( self.panel_out, style=wx.TE_READONLY|wx.TE_MULTILINE)
        self.stdout.SetSizerProps(proportion=1, expand=True)

        # self.stderr = wx.TextCtrl(self.panel2, style=wx.TE_READONLY|wx.TE_MULTILINE)
        self.stderr = wx.TextCtrl( self.panel_out, style=wx.TE_READONLY|wx.TE_MULTILINE)
        self.stderr.SetSizerProps(proportion=1, expand=True)
        self.stderr.SetForegroundColour(wx.RED)

        # add to the timer callback list:
        self.timerCallbacks.append(self.ShowIO)
        
    def RunCmd(self, event):
        if self.pid is None:
            self.txt_cmd.SetForegroundColour(wx.GREEN)
            self.process = wx.Process(self.panel)
            self.process.Redirect()
            self.pid = wx.Execute(self.cmd, wx.EXEC_ASYNC, self.process)
            print 'Executed:  %s' % (self.cmd)
            
    def Kill(self, event):
        if self.pid:
            print 'Killing: %s' % (self.cmd)
            wx.Process.Kill(self.pid)
            self.pid = None
            self.txt_cmd.SetForegroundColour(wx.BLUE)
        
           
    def ShowIO(self):
        if self.process is not None:

            stream = self.process.GetInputStream()
            while stream.CanRead():
                line = stream.read()
                line = line.strip()
                # print "O", line.__repr__()
                self.stdout.AppendText("\n"+line)

            stream = self.process.GetErrorStream()
            while stream.CanRead():
                line = stream.read()
                line = line.strip()
                # print "E", line.__repr__()
                self.stderr.AppendText("\n"+line)

    def RemovePanel(self, event):
        # remove this command to make room for the stuff we care about
        if self.pid is None:
            parent=self.panel.GetTopLevelParent() # Parent
            self.panel.Destroy() 
            self.stdout.Destroy() 
            self.stderr.Destroy() 
            self.panel_out.Destroy() 
            parent.SendSizeEvent()
 
    def ProcessEnded(self, event):
        if self.pid:
            self.txt_cmd.SetForegroundColour(wx.RED)
            self.ShowIO()

        self.process.Destroy()
        self.process = None

        print 'Process %s terminated: %s' % (self.pid, self.cmd)
        self.pid=None

def parse_args():
    parser = argparse.ArgumentParser(description='DVswitch manager.')
    parser.add_argument('--host')
    parser.add_argument('-p', '--port')
    parser.add_argument('-v', '--verbose', action="store_true" )
    parser.add_argument('-c', '--commands', nargs="*",
      help="command file" )

    args = parser.parse_args()
    return args

def mk_commands(args):

    host = "--host %s" % args.host if args.host else ''
    port = "--port %s" % args.port if args.port else ''
    hostport = ' '.join([host,port])

    # COMMANDS is caps cuz it is global
    # cuz I am not sure how to api the plugin like thing
    # where I use execfile() - it works.
    COMMANDS = [ ]

    for cmd_file in args.commands:
        execfile(cmd_file, locals())

    # strip trailing spaces which get passed as a parameter.
    commands = [cmd.strip() for cmd in COMMANDS]

    return commands

def main():
    
    args = parse_args()
    commands=mk_commands(args)
    
    app = wx.PySimpleApp()
    
    size=wx.GetDisplaySize()
    frame = sc.SizedFrame(None, title='dvs-mon',  pos=(1,1), size=(450, size[1]))
    panel = frame.GetContentsPane()

    for cmd in commands:
        cr = CommandRunner(cmd, panel)

    frame.Show()

    def OnTimer(evt):
        for cb in CommandRunner.timerCallbacks:
            cb()

    panel.Bind(wx.EVT_TIMER, OnTimer)
    timer = wx.Timer(panel)
    timer.Start(1000)

    app.MainLoop()

if __name__ == '__main__':
    main()
