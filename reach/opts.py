import argparse
from reach import host, commands

__parsed = None

def get_command():
    if not __parsed:
        __parse()
    return __parsed.cmd

def __parse():
    parser = argparse.ArgumentParser(description="reach")
    cmds_str = ','.join(commands.registry.keys())
    parser.add_argument('cmd',
                        help='The reach command to execute (%s)'%cmds_str,
                        metavar='CMD',
                        nargs='?',
                        choices=commands.registry.keys())
    parser.add_argument('host',
                        help='The host(s) connection chain',
                        nargs='+',
                        metavar='[user@]host',
                        type=host._str_to_host)
    parser.parse_args()
    __parsed = parser


def get_initial_host_chain():
    """ Check commandline arguments and build a host chain.
    """
    return ["randomhost"]

