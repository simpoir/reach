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

def _str_to_host(text):
    username, delim, host_and_parms = text.rpartition('@')
    new_host = dict()

    if username:
        new_host['username'] = username

    parms = host_and_parms.split(':')
    if parms:
        new_host['hostname'] = parms.pop(0)
        for keyval in parms:
            key, delim, val = keyval.partition('=')
            if key and val:
                new_host[key] = val

    return new_host

