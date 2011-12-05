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
from reach import settings

class ComplConfig(completor.Completor):
    def fill(self, host, requested):
        config = settings.Settings.get_instance()
        if config:
            host_data = config.hosts.get(host['hostname'], None)

            if host_data:
                hn = host_data.get('hostname', None)
                if hn:
                    host['hostname'] = hn
                pt = host_data.get('port', None)
                if pt:
                    host['port'] = pt
                un = host_data.get('username', None)
                if un:
                    host['username'] = un
                pw = host_data.get('password', None)
                if pw:
                    host['password'] = pw
                sc = host_data.get('scope', None)
                # don't overwrite the scope
                if sc:
                    host.setdefault('scope', sc)
                vi = host_data.get('visibility', None)
                # don't overwrite the scope
                if sc:
                    host['visibility'] = host.get('visibility', [])+sc.split(',')


    def lookup(self, scope):
        # TODO
        return []

completor.registry['config'] = ComplConfig()

