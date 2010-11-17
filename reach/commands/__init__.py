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
import sys
import readline
from reach import term


registry = {}

def register_command(name, help_line, command):
    """ Load the named command to the registry.

    name is used for binding to a commandline argument.
    help_line command usage.
    command is a callable which will be executed.
    """
    registry[name] = (help_line, command)


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


def execute_interactive():
    """ Runs the command mode once, reading the standard input for a command
    and executing it. Will return execution once a command has been executed
    or if an invalid command was passed.
    """
    old_completer = readline.get_completer()
    readline.set_completer(__readline_completer)
    readline.parse_and_bind('tab: complete')

    rows, cols = term.get_size()
    print('\n'*rows)
    term.set_pos(0, 0)

    # default raw mode is not readline friendly.
    # restore after saving display, for restoring is destructive
    term.restore_tty()

    cmd_name = raw_input('REACH:')

    cmd_args = [x for x in cmd_name.split(' ') if x != '']
    if cmd_args[0] in registry:
        registry[cmd_args[0]][1](cmd_args)
    else:
        sys.stdout.write('No such command')
        sys.stdout.write('[RETURN]')
        os.read(sys.stdin.fileno(), 1)
    term.restore_cursor()

    # return to raw_mode
    term.set_raw()
    readline.set_completer(old_completer)

    # FIXME this is the simplest way I found to redraw properly
    # send ctrl-l (redraw to the shell, assuming a shell is running)
    from reach import channel
    channel.Channel.get_instance().get_interactive_chan().send('')


def is_ninja():
    """ This function serves no purpose. The ninja is a lie. """
    pass


def __readline_completer(text, state):
    """ Callback for completing using readline.
    """
    i = 0
    for cmd_name in registry:
        if cmd_name.startswith(text):
            if i == state:
                return cmd_name
            i += 1
    return None


