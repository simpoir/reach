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


from reach import sshconnector, term, commands

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
        self.__ichan = None
        self.__prev_char = None


    _instance = None
    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = cls()
        return cls._instance


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


    def get_interactive_chan(self):
        """ Returns an interactive (shell) channel.

        A new channel is established if none exists.
        """
        if self.__ichan:
            return self.__ichan

        # else establish and create interactive channel
        term_size = term.get_size()
        self.__ichan = self.__chan.open_session()
        self.__ichan.get_pty('vt100', height=term_size[0], width=term_size[1])
        self.__ichan.invoke_shell()


    def run(self):
        """ Pass data between stdin -> channel, channel -> stdout
        Returns True if channel is still up, False if channel is broken.
        """
        if term.has_resized():
            term_size = term.get_size()
            self.__ichan.resize_pty(term_size[1], term_size[0])

        try:
            ready = select.select([self.__ichan, sys.stdin], [], [], 0.2)[0]
            if self.__ichan in ready:
                from_chan = self.__ichan.recv(1024)
                sys.stdout.write(from_chan)
                sys.stdout.flush()

            if sys.stdin in ready:
                from_console = sys.stdin.read(1)

                # catch command escape
                if from_console == '\r':
                    self.__prev_char = '\n'
                    self.__ichan.send(from_console)

                elif from_console == '~':
                    if self.__prev_char == '\n':
                        self.__prev_char = '~'
                    else:
                        self.__prev_char = None
                        self.__ichan.send(from_console)
                elif self.__prev_char == '~':
                    self.__prev_char = None
                    if from_console == '.':
                        commands.execute_interactive()
                    else:
                        self.__ichan.send('~'+from_console)
                else:
                    self.__prev_char = None
                    self.__ichan.send(from_console)

        except select.error:
            # Occurs when signal is received while select (E.G. term resize).
            # This is ok. Just continue as if nothing appened.
            # We'll resume select on next run().
            pass

        # Check if remote interactive channel has closed (shell exited).
        if self.__ichan.exit_status_ready():
            return False

        return True

