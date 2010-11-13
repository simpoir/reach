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

from reach import VERSION_MAJOR, VERSION_MINOR, VERSION_REVISION
from reach.commands import register_command


toothbrush = '''
   .
  ,|VVm"m"m|_________________,--vvv----------------.
  \-----------------------------------------------~'
                    Reach 2
'''

description = '''
Reach is a commandline tool to bounce ssh connections through one to
many hosts in order to access a system. It has a connection completion
API to be able to get and resolve a graph of hosts.
It also supports on-the-fly tunnelling.

Reach is also a trademark for an electric toothbrush, but this has obviously
nothing to do with this code.

Version 2 is a complete rewrite of a really nice tool.
'''

def version_cmd(args):
    print(toothbrush)
    print("Version %d.%d.%d" % (VERSION_MAJOR, VERSION_MINOR,
                                VERSION_REVISION))
    print()
    print(description)

register_command("version", version_cmd)

