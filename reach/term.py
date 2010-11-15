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

import tty
import termios
from fcntl import ioctl
import struct
import sys
import signal


__has_resized = False


def get_size():
    """ Returns the terminal size as a (rows, columns) tuple
    """
    # TIOCGWINSZ returns rows, columns, pixel_width, pixel height
    t_size = struct.pack('HHHH', 0, 0, 0, 0)
    t_size = ioctl(sys.stdout.fileno(),
                   termios.TIOCGWINSZ,
                   t_size)
    return struct.unpack('HHHH', t_size)[:2]


def has_resized():
    """ Returns whether the terminal has resized since last call to
    this function.
    """
    global __has_resized

    if __has_resized:
        # If signal occurs here, the returned value will still be true,
        # so this should be thread safe.
        __has_resized = False
        return True
    else:
        return False


# set resize handler that a
def __sig_resize_handler(*args):
    global __has_resized
    __has_resized = True
signal.signal(signal.SIGWINCH, __sig_resize_handler)


# Save terminal state
__term_state = termios.tcgetattr(sys.stdin.fileno())

def set_raw():
    termios.tcgetattr(sys.stdin.fileno())
    tty.setraw(sys.stdin.fileno())


def restore_tty():
    termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, __term_state)


def save_cursor():
    """ save the cursor position.
    """
    sys.stdout.write('\x1b7')
    sys.stdout.flush()


def restore_cursor():
    """ restore the cursor position of last save_cursor.
    Calling restore_cursor() without previous call to save_cursor() will lead
    to an unknown state.
    """
    sys.stdout.write('\x1b8')
    sys.stdout.flush()


def set_pos(row, column):
    """ Set the cursor position.
    """
    sys.stdout.write('\x1b[%d;%dH' % (row, column))
    sys.stdout.flush()


