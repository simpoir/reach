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

from reach.commands import register_command
from reach.channel import Channel

import paramiko

import os
import sys
import readline


lcwd = os.getcwd()
rcwd = '/'

def ls(sftp, args):
    content = sftp.listdir(rcwd)
    for i in content:
        print(i)

def lls(sftp, args):
    content = os.listdir(lcwd)
    for i in content:
        print(i)

def cd(sftp, args):
    global rcwd
    if len(args) < 2:
        print('USAGE: cd {path}')
        return
    path = ' '.join(args[1:])
    new_path = os.path.join(rcwd, path)
    try:
        sftp.chdir(new_path)
    except IOError, e:
        print(e)
        return
    rcwd = sftp.getcwd()

def lcd(sftp, args):
    global lcwd
    if len(args) < 2:
        print('USAGE: lcd {path}')
        return
    path = ' '.join(args[1:])
    new_path = os.path.join(lcwd, path)
    if not os.path.isdir(new_path):
        print('invalid directory')
        return
    lcwd = new_path

def put(sftp, args):
    if len(args) < 2:
        print('USAGE: put {path}')
        return

    path = ' '.join(args[1:])
    filename = os.path.split(path)[-1]
    remotename = os.path.join(rcwd, filename)
    localname = os.path.join(lcwd, args[1])
    try:
        sftp.put(localname, remotename, callback=_sftp_callback)
    except paramiko.SFTPError:
        print('aborted')
        return

def get(sftp, args):
    if len(args) < 2:
        print 'USAGE: get {path}'
        return
    path = ' '.join(args[1:])
    filename = os.path.split(path)[-1]
    remotename = os.path.join(sftp.getcwd(), filename)
    localname = os.path.join(lcwd, args[1])
    try:
        sftp.get(remotename, localname, callback=_sftp_callback)
    except paramiko.SFTPError:
        print('aborted')
        return


all_cmd = {
    'ls':ls,
    'cd':cd,
    'put':put,
    'get':get,
    'lls':lls,
    'lcd':lcd,
}


def _sftp_callback(transf, total):
    sys.stdout.write('\r\x1b[2K[%d/%d]'%(transf, total))
    sys.stdout.flush()


class sftp_completer:
    def __init__(self, sftp):
        self.sftp = sftp

    def __call__(self, search, index):
        i = 0
        if readline.get_begidx() == 0:
            # complete command
            for key in all_cmd.keys():
                if key.startswith(search):
                    if index == i:
                        return key
                    i += 1
            return None
        else:
            buf = readline.get_line_buffer()
            cmd, delim, filepath = buf.partition(' ')
            path_components = os.path.split(filepath)
            search = path_components[-1]
            filepath = os.path.join(*path_components[:-1])
            if cmd in ('cd', 'get'):
                # complete remote
                if index == 0:
                    self.remote_list = filter(lambda x:x.startswith(search),
                            self.sftp.listdir(os.path.join(rcwd, filepath)))
                    # TODO write a command line parser as this is almost too
                    # horrible.
                    # The following cuts the already completed part to the last
                    # space, takes that lengh and remove it from completion
                    # choices. Example:
                    # foo bar zoo far
                    # foo bar z<tab>
                    #        ^- rpartition up to here 
                    #  drop  | keep
                    return self.remote_list[index][len(search.rpartition(' ')[0]):].strip()

            elif cmd in ('put', 'lcd'):
                # complete locally
                for key in os.listdir(os.path.join(lcwd, filepath)):
                    if key.startswith(search):
                        if index == i:
                            return key[len(search.rpartition(' ')[0]):].strip()
                        i += 1
                return None



def sftp_cmd(*args):
    sftp = Channel.get_instance().get_transport().open_sftp_client()

    old_completer = readline.get_completer()
    readline.set_completer(sftp_completer(sftp))
    old_delim = readline.get_completer_delims()
    readline.set_completer_delims(' /')
    global rcwd

    try:
        try:
            cmd = raw_input('SFTP> ')
        except EOFError:
            return
        except KeyboardInterrupt:
            return
        while not cmd or not 'quit'.startswith(cmd):
            args = [x for x in cmd.split(' ') if x]
            if args and args[0] in all_cmd:
                all_cmd[args[0]](sftp, args)
            else:
                print('invalid command')
            try:
                cmd = raw_input('SFTP> ')
            except EOFError:
                return
            except KeyboardInterrupt:
                return
    finally:
        readline.set_completer(old_completer)
        readline.set_completer_delims(old_delim)


help_line = 'Transfer files.'

register_command("sftp", help_line, sftp_cmd)

