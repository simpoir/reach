# Reach, the remote acccess tool
# Copyright (C) 2011  Simon Poirier <simpoir@gmail.com>
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
from SocketServer import TCPServer, BaseRequestHandler, ThreadingMixIn

import sys
import threading
import select
from functools import partial



def setup_lfwd_cmd(args):

    if len(args) != 4:
        sys.stdout.write(
            'syntax: lfwd {local port} {remote host} {remote port}\n')
        sys.stdout.write('[RETURN]')
        sys.stdout.flush()
        sys.stdin.readline()
        return
    _, lport, rhost, rport = args


    socks_port = int(lport)
    socks_svr = SocksServer(('127.0.0.1', socks_port),
                            partial(LocalHandler, dst=rhost, dport=rport))

    sys.stdout.write('listening on port %d\n'%socks_port)
    sys.stdout.write('[RETURN]')
    sys.stdout.flush()
    sys.stdin.readline()

    # Start a thread with the server -- that thread will then start one
    # more thread for each request
    server_thread = threading.Thread(target=socks_svr.serve_forever)
    # Exit the server thread when the main thread terminates
    server_thread.setDaemon(True)
    server_thread.start()


help_line = 'forward local port to remote channel.'

register_command("lfwd", help_line, setup_lfwd_cmd)

# threaded tcp server mixin
class SocksServer(ThreadingMixIn, TCPServer):
    pass

class LocalHandler(BaseRequestHandler, object):
    def __init__(self, request, client_address, server, dst, dport):
        self.__dst = dst
        self.__dport = dport
        super(LocalHandler, self).__init__(request, client_address, server)

    def handle(self):
        from reach.channel import Channel

        chan = Channel.get_instance().get_chan(dict(
            hostname=self.__dst, port=self.__dport))

        while True:
            readable = select.select([self.request, chan], [], [], 10)[0]
            if chan in readable:
                r_data = chan.recv(1024)
                self.request.send(r_data)
                if not r_data:
                    return
            elif self.request in readable:
                r_data = self.request.recv(1024)
                chan.send(r_data)
                if not r_data:
                    return


