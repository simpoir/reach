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

