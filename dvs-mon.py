#!/usr/bin/python
#
# -*- coding: utf-8 -*-
# vim: set ts=4 sw=4 et sts=4 ai:

import argparse
import time

import os
import fcntl
import subprocess

import wx
# import wx.lib.sized_controls as sc
# import wx.lib.inspection

DARKGREEN = wx.Colour(0,196,0)

def set_nonblock(fd):
    f1 = fcntl.fcntl(fd.fileno(), fcntl.F_GETFL)
    fcntl.fcntl(fd.fileno(), fcntl.F_SETFL, f1|os.O_NONBLOCK)

class CommandRunner(object):

    """
    given a shell command
    adds a panel to the main window with the following:
    display the command
    buttons to run/kill the command
    X to remove the panel, but only if the command is not running
    multiline text areas for stdout, stderr
    """

    process = None
    detail = True
    keepalive = False

    def __init__(self, frame, startdelay, cmd, args):

        self.cmd = cmd
        self.frame = frame

        if args.keepalive:
            self.keepalive = args.keepalive
            # extra delay to spread out startup
            self.deadtime = startdelay
        else:
            self.keepalive = False

        # outer panel to hold the 3 parts:
        #  cmd+buttons, stdout, stderr

        panel_cr = wx.Panel(frame)
        panel_cr.Sizer = wx.BoxSizer(wx.VERTICAL)
        self.cr_sizer = frame.Sizer.Add(panel_cr, 10, wx.EXPAND)
        self.panel_cr = panel_cr

        # cmd+buttons
        panel_cmd = wx.Panel(panel_cr)
        panel_cmd.Sizer = wx.BoxSizer(wx.HORIZONTAL)
        panel_cr.Sizer.Add(panel_cmd, 0, wx.EXPAND)

        self.panel_cmd = panel_cmd

        self.txt_cmd = wx.TextCtrl(
                panel_cmd, value=self.cmd.label, style=wx.TE_READONLY)
        self.txt_cmd.SetForegroundColour(wx.WHITE)
        self.txt_cmd.SetBackgroundColour(wx.BLUE)
        panel_cmd.Sizer.Add(self.txt_cmd, 1, wx.EXPAND)

        btn1 = wx.Button(panel_cmd, label='Run', size=(45, -1))
        panel_cmd.Sizer.Add(btn1, 0, wx.EXPAND)
        btn1.Bind(wx.EVT_BUTTON, self.RunCmd)

        btn2 = wx.Button(panel_cmd, label='Kill', size=(45,-1))
        panel_cmd.Sizer.Add(btn2, 0, wx.EXPAND)
        btn2.Bind(wx.EVT_BUTTON, self.Kill)

        btn3 = wx.Button(panel_cmd, label='Detail', size=(60,-1))
        panel_cmd.Sizer.Add(btn3, 0, wx.EXPAND)
        btn3.Bind(wx.EVT_BUTTON, self.Detail)

        btn4 = wx.Button(panel_cmd, label='X', size=(25,-1))
        panel_cmd.Sizer.Add(btn4, 0, wx.EXPAND)
        btn4.Bind(wx.EVT_BUTTON, self.RemovePanel)

        # sdtout
        stdout = wx.TextCtrl(
                panel_cr, style=wx.TE_READONLY|wx.TE_MULTILINE)
        self.stdout_sizer = panel_cr.Sizer.Add(stdout, 1, wx.EXPAND)
        self.stdout = stdout

        # stderr
        stderr = wx.TextCtrl(
                panel_cr, style=wx.TE_READONLY|wx.TE_MULTILINE)
        self.stderr_sizer = panel_cr.Sizer.Add(stderr, 1, wx.EXPAND)
        stderr.SetForegroundColour(wx.RED)
        self.stderr = stderr

        # start a timer to check for stdout/err
        panel_cr.Bind(wx.EVT_TIMER, self.OnTimer)
        self.timer = wx.Timer( panel_cr)
        self.timer.Start(100)


    def Detail(self, event=None, show=None):
        # show/hide stdout/err

        if show is None:
            # flip state
            self.detail = not self.detail
        else:
            if self.detail == show:
                # nothing to do, don't animate, it looks weird.
                return
            else:
                self.detail = show


        def animate(sequence):
            for i in sequence:
                self.cr_sizer.SetProportion(i)
                self.frame.Layout()
                self.frame.Update()
                wx.Yield()

        if self.detail:
            # show detail on display
            # restore to normal size
            self.stdout.Show()
            self.stderr.Show()
            animate(range(1, 11))
            # self.cr_sizer.SetProportion(1)

        else:
            # remove detail from display
            # squish
            animate(reversed(range(1, 11)))
            self.stdout.Hide()
            self.stderr.Hide()
            self.cr_sizer.SetProportion(0)

        self.frame.Layout()
        self.frame.Refresh()


    def Append(self, ctrl, line):
        ctrl.AppendText(line)

    def MarkOuts(self, line):
        self.Append(self.stdout,line+"\n")
        self.Append(self.stderr,line+"\n")


    def RunCmd(self, event=None):
        if self.process is None:
            self.MarkOuts("Starting...")
            self.txt_cmd.SetBackgroundColour(DARKGREEN)
            self.process = subprocess.Popen(
                self.cmd.command,
                stdout = subprocess.PIPE,
                stderr = subprocess.PIPE,
                shell = True,
                )
            set_nonblock(self.process.stdout)
            set_nonblock(self.process.stderr)
            self.MarkOuts("Started.")
            print 'Executed:  %s' % (self.cmd.command)

    def Kill(self, event):
        if self.process is not None:
            self.MarkOuts("Killing...")
            print 'Killing: %s' % (self.cmd.command)
            self.process.kill()
            self.MarkOuts("Killed.")
            self.txt_cmd.SetBackgroundColour(wx.BLUE)
            self.keepalive = 0

    def ReadIO(self):
        try:
            self.Append(self.stdout, self.process.stdout.read())
            self.Append(self.stderr, self.process.stderr.read())
        except IOError, e:
            pass

    def PollProcess(self):
        if self.process is not None:
            self.ReadIO()

            retcode = self.process.poll()
            if retcode is not None:
                self.ProcessEnded(retcode)

    def KeepAlive(self):
        if self.keepalive:
            if self.deadtime:
                # If process died, leave it dead for X timer cycles
                self.deadtime-=1
            else:
                self.RunCmd()

    def OnTimer(self,event):
        self.PollProcess()
        self.KeepAlive()

    def ProcessEnded(self, retcode):
        if self.process is not None:
            self.txt_cmd.SetBackgroundColour(wx.RED)
            # make sure there is no more stdout/err
            self.ReadIO()
            self.MarkOuts("DIED!")
            # expand the UI
            self.Detail(show=True)

        self.process = None

        print 'DIED: %s' % (self.cmd.command)
        self.deadtime = self.keepalive


    def RemovePanel(self, event):
        if self.process is None:
            parent=self.panel_cr.GetTopLevelParent()
            self.timer.Stop()
            self.timer.Destroy()
            self.panel_cr.Destroy()
            parent.SendSizeEvent()

class Command(object):
    def __init__ (self, command, label = None):
        # strip trailing spaces which get passed as a parameter.
        self.command = command.strip ()

        if label is None:
            self.label = self.command
        else:
            self.label = label.strip ()

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
            execfile(cmd_file, {'Command': Command}, locals())
    else:
        # for testing.
        COMMANDS=[
            Command('ping -i .3 127.0.0.1',         'Ping .3s'),
            Command('ping -i 1 127.0.0.1',          'Ping 1s'),
            Command('ping localhost',               'Ping localhost'),
            Command('ssh localhost ping localhost', 'Ping localhost (SSH)'),
            Command('ping -c 5 -i .5 localhost'),
            Command('ping -h',                      'Ping help')
        ]

    return COMMANDS

def parse_args():
    parser = argparse.ArgumentParser(description='DVswitch manager.')
    parser.add_argument('--host' )
    parser.add_argument('-p', '--port' )
    parser.add_argument('-k', '--keepalive', type=int )
    parser.add_argument('-c', '--commands', nargs="*",
      help="command file" )
    parser.add_argument('-s', '--show-all-detail', action="store_true" ,
            default=False)
    parser.add_argument('-v', '--verbose', action="store_true" )

    args = parser.parse_args()
    return args

def main():

    args = parse_args()
    commands=mk_commands(args)

    app = wx.App(False)

    size = wx.GetDisplaySize()
    frame = wx.Frame(
            None, title='dvs-mon',  pos=(1,1), size=(450, size[1]-100))
    frame.Sizer = wx.BoxSizer(wx.VERTICAL)

    startdelay=args.keepalive
    for cmd in commands:
        cr = CommandRunner( frame, startdelay, cmd, args )
        if args.show_all_detail:
            cr.Detail(cr,show=True)
        else:
            cr.Detail(cr,show=False)
        if args.keepalive is not None:
            startdelay+=args.keepalive/2

    # show stdout/err of last command:
    cr.Detail(cr,show=True)

    frame.Show()

    # wx.lib.inspection.InspectionTool().Show()

    app.MainLoop()

if __name__ == '__main__':
    main()
