#!/usr/bin/python
#
# -*- coding: utf-8 -*-
# vim: set ts=4 sw=4 et sts=4 ai:

import argparse
import atexit
import os
import fcntl
import select
import signal
import subprocess
import sys
import threading
import time

import wx
# import wx.lib.sized_controls as sc
# import wx.lib.inspection

# Make sure everything dies when I die....
KILLME = []
def cleanup():
    for p in KILLME:
        p.cleanup()
    return True
atexit.register(cleanup)


DARKGREEN = wx.Colour(0,196,0)

class PollingThread(threading.Thread):
    """Watches the stdout and stderr of a command and appends the output to a wxWidget.

    FIXME: Currently only supports one command per thread but this is wasteful
    as epoll supports a bazillion sockets. Only reason multiple threads is for
    the process tracking.
    """

    MASK = select.EPOLLIN | select.EPOLLPRI | select.EPOLLERR | select.EPOLLHUP

    def __init__(self, command, stdout, stderr, callback):
        threading.Thread.__init__(self)
        # We terminate when the program terminates
        self.setDaemon(True)

        KILLME.append(self)

        self._status = []
        self.status("STARTING")

        # Move the subprocess into it's own process group
        def new_process_group():
            import os
            os.setpgrp()

        # Create the output process
        self.process = subprocess.Popen(
            command,
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE,
            shell = True,
            preexec_fn = new_process_group,
            )

        # Wait for the process to move into it's own process group, then capture
        # the process group.
        while True:
            self.process_group = os.getpgid(self.process.pid)
            if self.process_group == os.getpgid(0):
                continue
            break

        self.epoll = select.epoll()
        self.fd_to_output = {}

        self.callback = callback

        self.register(self.process.stdout, stdout)
        self.register(self.process.stderr, stderr)

        self.status("RUNNING")

    def cleanup(self):
        print "Cleanup", self
        try:
            self.kill()
        except Exception, e:
            print e

        try:
            self.poll()
        except Exception, e:
            print e

        time.sleep(0.1)
        try:
            self.killhard()
        except Exception, e:
            print e

        try:
            self.poll()
        except Exception, e:
            print e

    def status(self, status):
        self._status.append((status, time.time()))

    def register(self, pipe, output):
        # Set the file descriptor to be non-blocking as we don't know how much
        # is ready to read but don't want to read a single byte at the time.
        f1 = fcntl.fcntl(pipe.fileno(), fcntl.F_GETFL)
        fcntl.fcntl(pipe.fileno(), fcntl.F_SETFL, f1|os.O_NONBLOCK)

        # Create a mapping so we can get back to the file object
        self.fd_to_output[pipe.fileno()] = (pipe, output)

        # Register the file descriptor on the epoll object.
        self.epoll.register(pipe.fileno(), self.MASK)

    def run(self):
        # While the process is running
        while self.process.returncode is None:
            # print self._status, time.time() - self._status[-1][-1]
            # Kill roughly if it's taking to long to kill...
            if self._status[-1][0] == "KILLING" and (
                    time.time() - self._status[-1][-1]) > 5.0:
                self.killhard()

            self.poll()

        KILLME.remove(self)

        # One last poll to get the remaining stuff
        self.status("DIEING")
        self.poll()
        self.status("DEAD")

        # Tell people the process died
        wx.CallAfter(self.callback, self.process.returncode)

    def kill(self):
        self.status("KILLING")
        # Kill the program nicely first
        os.killpg(self.process_group, signal.SIGTERM)

    def killhard(self):
        try:
            # Stop all the processes first (so they don't keep spawning new
            # processes in this group).
            os.killpg(self.process_group, signal.SIGSTOP)
        except OSError, e:
            print self._status
            print e

        try:
            # Kill all the processes in the process group we created.
            os.killpg(self.process_group, signal.SIGKILL)
        except OSError, e:
            print self._status
            print e

    def poll(self):
        self.process.poll()

        events = self.epoll.poll(0.1)
        for fd, event in events:
            if event == select.EPOLLHUP:
                self.epoll.unregister(fd)

            pipe, output = self.fd_to_output[fd]
            try:
                data = pipe.read()
            except IOError, e:
                wx.CallAfter(output.Append, "***Internal Error***: %s" % e)

            wx.CallAfter(output.Append, data)
            # Everytime we callout, we sleep for a little bit to stop wxWidgets
            # getting locked up dealing with CallAfter events (as we can post
            # them quicker then wxWidgets deals with them).
            time.sleep(0.1)


class CommandRunner(object):

    """
    given a shell command
    adds a panel to the main window with the following:
    display the command
    buttons to run/kill the command
    X to remove the panel, but only if the command is not running
    multiline text areas for stdout, stderr
    """

    poller = None
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

        class TextCtrlWithAppend(wx.TextCtrl):
            def Append(self, line):
                if self.GetLastPosition() > 1e3:
                    self.Remove(0, len(line))
                self.AppendText(line)

        self.frame.Bind(wx.EVT_CLOSE, self.Kill)

        # sdtout
        stdout = TextCtrlWithAppend(
                panel_cr, style=wx.TE_READONLY|wx.TE_MULTILINE)
        self.stdout_sizer = panel_cr.Sizer.Add(stdout, 1, wx.EXPAND)
        self.stdout = stdout

        # stderr
        stderr = TextCtrlWithAppend(
                panel_cr, style=wx.TE_READONLY|wx.TE_MULTILINE)
        self.stderr_sizer = panel_cr.Sizer.Add(stderr, 1, wx.EXPAND)
        stderr.SetForegroundColour(wx.RED)
        self.stderr = stderr

        self.poller = None

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

    def MarkOuts(self, line):
        self.stdout.Append(line+"\n")
        self.stderr.Append(line+"\n")

    def RunCmd(self, event=None):
        if self.poller is None:
            self.MarkOuts("Starting...")
            self.txt_cmd.SetBackgroundColour(DARKGREEN)

            self.poller = PollingThread(
                self.cmd.command, self.stdout, self.stderr, self.ProcessEnded)

            self.MarkOuts("Started.")
            print 'Executed:  %s' % (self.cmd.command)
            self.poller.start()

    def _KillMore(self, event, poller):

        self.MarkOuts("Sending KILL...")
        self.poller.kill()
        self.MarkOuts("Sent.")

    def Kill(self, event):
        self.keepalive = 0

        if self.poller is not None:
            self.MarkOuts("Sending TERM...")
            print 'Killing: %s' % (self.cmd.command)
            self.poller.kill()

        event.Skip()

    def KeepAlive(self):
        if self.keepalive:
            if self.deadtime:
                # If process died, leave it dead for X timer cycles
                self.deadtime-=1
            else:
                self.RunCmd()

    def OnTimer(self,event):
        self.KeepAlive()

    def ProcessEnded(self, retcode):
        if self.poller is not None:
            self.txt_cmd.SetBackgroundColour(wx.RED)
            self.MarkOuts("DIED! with %s" % retcode)
            # expand the UI
            self.Detail(show=True)

        self.poller = None
        print 'DIED: %s with %s' % (self.cmd.command, retcode)
        self.deadtime = self.keepalive

    def RemovePanel(self, event):
        if self.poller is None:
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
            Command('ping -h',                      'Ping help'),
            Command('python dontdie.py',            'I don\'t die!'),
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

app = None
def main():
    global app

    args = parse_args()
    commands=mk_commands(args)

    # Clear the default signal handlers so control ends up back in Python and we
    # can cleanup running processes.
    app = wx.App(clearSigInt=True)

    # WARNING: This code needs to occur right after the app is created and
    # before the main loop starts.
    #-------------------------------------------------------------------------
    # Set up signal handlers which terminate the application when they occur.
    import signal
    # Create human names for the signals
    signal.names = dict(
            (k, v) for v, k in signal.__dict__.iteritems() if v.startswith('SIG'))
    def signal_cleanup(sig, frame):
        print "Caught %s, exiting" % signal.names[sig]
        wx.CallAfter(app.Exit)
    signal.signal(signal.SIGTERM, signal_cleanup)
    signal.signal(signal.SIGINT, signal_cleanup)

    # Signals are only delivered when wxPython hands back to the Python
    # interpretor, this stupid hack forces that to happen once every 100
    # milliseconds.
    def ticker(*args):
        pass
    app.ticker = wx.PyTimer(ticker)
    app.ticker.Start(100)
    #-------------------------------------------------------------------------

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
