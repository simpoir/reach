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
from SocketServer import TCPServer, BaseRequestHandler, ThreadingMixIn

import sys
import threading
import struct
import select


socks_svr = None
socks_port = None

def setup_socks_cmd(args):
    global socks_svr, socks_port

    if len(args) != 2:
        sys.stdout.write('syntax: socks {port}\n')
        sys.stdout.write('[RETURN]')
        sys.stdout.flush()
        sys.stdin.readline()
        return

    if socks_port != None:
        sys.stdout.write('socks already listening on port %d\n'%socks_port)
        sys.stdout.write('[RETURN]')
        sys.stdout.flush()
        sys.stdin.readline()
        return

    socks_port = int(args[1])
    socks_svr = SocksServer(('127.0.0.1', socks_port), SocksHandler)

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


help_line = 'bind a socks proxy to specified port.'

register_command("socks", help_line, setup_socks_cmd)

# threaded tcp server mixin
class SocksServer(ThreadingMixIn, TCPServer):
    pass

class SocksHandler(BaseRequestHandler):
    socks4header = struct.Struct('!BBH4s')

    def handle(self):
        from reach.channel import Channel
        data = self.request.recv(self.socks4header.size)
        s_ver, s_cmd, s_port, s_ip = self.socks4header.unpack(data)

        chan = None
        if s_ver == 0x04 and s_cmd == 0x01:
            # v4 connect

            # receive null terminated user id
            user_id = ''
            c = self.request.recv(1)
            while c != '\x00':
                c = self.request.recv(1)
            del c

            # convert to string ip
            dst_ip = '.'.join([str(ord(x)) for x in s_ip])
            chan = Channel.get_instance().get_chan(dict(
                hostname=dst_ip, port=s_port))
            self.request.send(self.socks4header.pack(0, 0x5a, 0, 'moo!'))
        else:
            # V4 error
            self.request.send(self.socks4header.pack(0, 0x5b, 0, 'oops'))
            print 'unsupported socks connection'
            return

        # TODO relay data
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


