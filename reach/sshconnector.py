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
from reach import completor

import paramiko
import os

class SshConnector(object):
    # basic required args
    required = ('hostname', 'port', 'username')

    # default completion mapping
    defaults = (('port', '22'),
                ('username', os.environ.get('USER')))

    class __default_completor(completor.Completor):
        def fill(self, host, requested):
            for parm,val in SshConnector.defaults:
                if not host.get(parm, False):
                    host[parm] = val

        def lookup(self, host):
            return []


    def connect(self, host, channel):
        """ Connect to host using channel as spawn shell.

        This will be called recursively on a channel.
        """
        #print("i would connect to %(hostname)s on port %(port)s with user %(username)s and password %(password)s"%host)
        #raise NotImplementedError()

        chan = channel.get_chan(host)
        transport = paramiko.Transport(chan)
        transport.connect(username=host['username'],password=host['password'])
        channel.set_chan(transport)
        print('succeeded connnecting to %s'%host['hostname'])

    def get_required(self, host):
        """ Returns a list of required host attributes to connect to host.

        Returned attributes may be already assigned in host.
        """
        if host.has_key('sshkey') and host.get('sshkey') != None:
            return SshConnector.required + ('sshkey',)

        return SshConnector.required + ('password',)


    def get_defaults_completor(self):
        """ Returns a Completor object for this connector's defaults.
        """
        return SshConnector.__default_completor()

