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

import argparse
from reach import host, commands

__parsed = None

def get_command():
    if not __parsed:
        __parse()
    return __parsed.cmd

def __parse():
    global __parsed
    parser = argparse.ArgumentParser(description="reach")
    cmds_str = ','.join(commands.registry.keys())
    parser.add_argument('host',
                        help='The host(s) connection chain',
                        nargs='+',
                        metavar='[user@]host',
                        type=host._str_to_host)
    __parsed = parser.parse_args()


def get_initial_host_chain():
    """ Check commandline arguments and build a host chain.
    """
    if not __parsed:
        __parse()

    return __parsed.host

