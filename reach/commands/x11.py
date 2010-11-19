# Reach, the remote acccess tool
# Copyright (C) 2010  Simon Poirier <simpoir@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from reach.commands import register_command
from reach.channel import Channel

import select
import socket
from threading import Thread
import os


def x11_thread(xsock, channel):
    while True:
        readable, w, x = select.select([xsock, channel], [], [], 100)
        if xsock in readable:
            data = xsock.recv(512)
            if not data:
                return
            channel.send(data)
        if channel in readable:
            data = channel.recv(512)
            if not data:
                return
            xsock.send(data)


def x11_handler(channel, orig_addr, server_addr):
    xsock = None
    # FIXME handle errors
    disp_host, disp_no = os.environ.get('DISPLAY').split(':')
    disp_no = disp_no.split('.')[0]
    if not disp_host:
        xsock = socket.socket(socket.AF_UNIX)
        xsock.connect('/tmp/.X11-unix/X'+disp_no)
    else:
        xsock = socket.socket()
        xsock.connect((disp_host, 6000+int(disp_no)))

    thr = Thread(target=x11_thread, args=(xsock, channel))
    thr.setDaemon(True)
    thr.start()


def x11_cmd(*args):
    # FIXME find usable port
    x_port = 10

    t = Channel.get_instance().get_transport()
    t.request_port_forward('127.0.0.1', 6000+x_port, x11_handler)
    Channel.get_instance().get_interactive_chan().send(
        'export DISPLAY=localhost:%d\n'%x_port)

help_line = 'Tunnel X11 connections locally.'

register_command("x11", help_line, x11_cmd)

