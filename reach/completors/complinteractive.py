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

import getpass


ASK_RESOLUTION = False

class ComplInteractive(completor.Completor):
    def fill(self, host, requested):
        """ Spam user about requested params. The rest doesn't matter.
        """

        # FIXME I don't see a backend without a hostname, but I don't like
        # direct depenencies to host attributes.
        host_name = host.get('hostname', 'unknown host')
        user_name = host.get('username', 'unknown user')

        for req_name in requested:
            if (not host.has_key(req_name)) or (host.get(req_name) == None):
                if req_name == 'password':
                    val = getpass.getpass("'%s@%s' %s: " % (user_name,
                                                            host_name,
                                                            req_name))
                else:
                    val = raw_input("'%s' %s: " % (host_name, req_name))
                host[req_name] = val

    def lookup(self, host):
        """ Does not lookup anything; user already completed using the sys.argv
        """
        return []

completor.registry['interactive'] = ComplInteractive()

