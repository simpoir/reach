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
from getpass import getpass
import urllib2, urllib


class ComplEps(completor.Completor):
    def init(self):
        if hasattr(self, '_host'):
            return
        self.skip = False
        config = settings.Settings.get_instance()
        if not config:
            return
        info = config.xmldoc.getElementsByTagName('epscompletor')
        self._host = info and info[0].getAttribute('host') \
                or raw_input('eps url:')
        self._data = {'username':info and info[0].getAttribute('username') \
                      or raw_input('eps user:'),
                      'password':info and info[0].getAttribute('password') \
                      or getpass('eps password:'),
                     }

    def fill(self, host, requested):
        self.init()

        if not self._data.get('password') or self.skip:
            return
        config = settings.Settings.get_instance()
        eid = None
        if config:
            host_data = config.hosts.get(host['hostname'], None)

            if host_data and host_data.get('epsid'):
                eid = host_data.get('epsid')
        if not eid:
            # search
            pass
        if eid:
            self._data['id'] = eid
            try:
                u = urllib2.urlopen(self._host+'/api/GetPassword',
                                    urllib.urlencode(self._data))
                host['password'] = u.read().strip()
            except Exception, e:
                self.skip = True
                print "Error fetching eps password."
                print e


    def lookup(self, scope):
        # TODO
        return []

completor.registry['eps'] = ComplEps()

