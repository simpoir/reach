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

