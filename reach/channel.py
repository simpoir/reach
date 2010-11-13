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


from reach import sshconnector

import sys
import select
import socket

class Channel(object):
    """ Represents a channel, I.E. a IO stream to a shell or something
    that is at least interactive enough for SshConnector to do something with.
    """
    def __init__(self):
        super(Channel, self).__init__()

        self.__chan = None

    def get_chan(self, host):
        if not self.__chan:
            sock = socket.socket()
            sock.connect((host['hostname'], int(host['port'])))
            return sock
        else:
            return self.__chan.open_channel(
                'direct-tcpip',
                (host['hostname'], int(host['port'])),
                ('0.0.0.0', 9090))

    def set_chan(self, newchan):
        self.__chan = newchan

    def chain_connect(self, chain):
        conn = sshconnector.SshConnector()
        for link in chain:
            conn.connect(link, self)

        # FIXME keep chan and save interacivechan
        self.__chan = self.__chan.open_session()
        self.__chan.get_pty('vt100', 80, 24)
        self.__chan.invoke_shell()


    def run(self):
        """ Pass data between stdin -> channel, channel -> stdout
        Returns True if channel is still up, False if channel is broken.
        """
        if len(select.select([self.__chan], [], [], 0.2)[0]) > 0:
            from_chan = self.__chan.recv(1024)
            sys.stdout.write(from_chan)
            sys.stdout.flush()

        if len(select.select([sys.stdin], [], [], 0.5)[0]) > 0:
            from_console = sys.stdin.read(1)

            # catch EOF
            if not from_console or from_console == '\x04':
                return False
            self.__chan.send(from_console)

        # TODO detect conn end
        return True

