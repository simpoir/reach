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

from reach.commands import register_command, registry

import sys

def help_cmd(*args):
    for cmd_name, cmd in registry.items():
        print(cmd_name)
        print('\t'+cmd[0])
    sys.stdout.write('[RETURN]')
    sys.stdout.flush()
    sys.stdin.readline()

help_line = 'Show this help.'

register_command("help", help_line, help_cmd)

