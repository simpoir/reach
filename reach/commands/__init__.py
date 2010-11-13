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

import os

registry = {}

def register_command(name, command):
    """ Load the named command to the registry.

    name is used for binding to a commandline argument.
    command is a callable which will be executed.
    """
    registry[name] = command


def load_cmds():
    """ Load all commands modules located in the reach.commands package.

        Command modules are expected to call register_command() on themselves.
    """
    registry.clear()
    cmdnames = os.listdir(os.path.dirname(__file__))
    for cmdname in cmdnames:
        if (not cmdname.endswith('.py')) or (cmdname[0] == '_'):
            continue
        cmd_mod_name = cmdname.rpartition('.')[0]
        cmd_mod = __import__('reach.commands.'+cmd_mod_name, fromlist=[True])

load_cmds()


def is_ninja():
    """ This function serves no purpose. The ninja is a lie. """
    pass

