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
    socks4header = struct.Struct('!H4s')
    socks4response = struct.Struct('!BBH4s')
    socks5response = struct.Struct('!BBBB')

    def handle(self):
        from reach.channel import Channel
        s_ver = ord(self.request.recv(1))

        chan = None
        if s_ver == 0x04:
            # v4 connect
            s_cmd = ord(self.request.recv(1))
            if s_cmd != 0x01:
                # TODO support bind command
                # return V4 error
                self.request.send(self.socks4response.pack(0, 0x5b, 0, 'oops'))
                return

            data = self.request.recv(self.socks4header.size)
            s_port, s_ip = self.socks4header.unpack(data)

            # convert to string ip
            dst_ip = '.'.join([str(ord(x)) for x in s_ip])

            # receive null terminated user id
            user_id = ''
            c = self.request.recv(1)
            while c != '\x00':
                user_id += c
                c = self.request.recv(1)
            del c

            if s_ip.startswith('\x00\x00\x00') and s_ip[3] != '\x00':
                # v4a extension
                dst_ip = ''
                c = self.request.recv(1)
                while c != '\x00':
                    dst_ip += c
                    c = self.request.recv(1)
                del c

            chan = Channel.get_instance().get_chan(dict(
                hostname=dst_ip, port=s_port))
            self.request.send(self.socks4response.pack(0, 0x5a, 0, 'moo!'))
        elif s_ver == 0x05:
            # socks v5
            nb_auth = self.request.recv(1)
            auths = []
            for i in xrange(ord(nb_auth)):
                auths.append(ord(self.request.recv(1)))
            if 0x00 in auths:
                # supports no-auth connections
                # return choice of no-auth
                self.request.send('\x05\x00')
            else:
                self.request.send('\x05\xFF')
                return

            # get request
            s_ver = self.request.recv(1)
            if s_ver != '\x05': 
                print 'expected v5, got '+repr(s_ver)
            s_cmd = self.request.recv(1)
            if s_cmd != '\x01': pass # TODO bind
            s_nul = self.request.recv(1)
            s_add = self.request.recv(1)
            s_ip = ''
            dst_ip = ''
            if s_add == '\x01':
                # ipv4
                s_ip = self.request.recv(4)
                # convert to string ip
                dst_ip = '.'.join([str(ord(x)) for x in s_ip])
            elif s_add == '\x03':
                # domain name
                l = ord(self.request.recv(1))
                dst_ip = self.request.recv(l)
                del l
                s_ip = dst_ip
            elif s_add == '\x04':
                # ipv6
                s_ip = self.request.recv(16)
                # convert to string ip
                dst_ip = '.'.join([str(ord(x)) for x in s_ip])
            else:
                return # malformed
            s_prt = struct.unpack('!H', self.request.recv(2))[0]

            chan = Channel.get_instance().get_chan(dict(
                hostname=dst_ip, port=s_prt))
            # request granted
            self.request.send(
                self.socks5response.pack(0x05, 0x00, 0x00, ord(s_add)))
            self.request.send(s_ip)
            self.request.send(struct.pack('!H', s_prt))
        else:
            # V4 error
            self.request.send(self.socks4response.pack(0, 0x5b, 0, 'oops'))
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


