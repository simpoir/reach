from reach import sshconnector

import sys
import select
import pexpect

class Channel(object):
    """ Represents a channel, I.E. a IO stream to a shell or something
    that is at least interactive enough for SshConnector to do something with.
    """
    def __init__(self):
        super(Channel, self).__init__()
        self.__chan = pexpect.spawn('/bin/sh', env={})


    def get_io(self):
        return self.__chan


    def chain_connect(self, chain):
        conn = sshconnector.SshConnector()
        for link in chain:
            conn.connect(link, self)


    def run(self):
        """ Pass data between stdin -> channel, channel -> stdout
        Returns True if channel is still up, False if channel is broken.
        """
        try:
            from_proc = self.__chan.read_nonblocking(1024, 0.2)
            sys.stdout.write(from_proc)
            sys.stdout.flush()
        except pexpect.TIMEOUT: pass

        sys.stdin.flush()
        if len(select.select([sys.stdin], [], [], 0.5)[0]) > 0:
            from_console = sys.stdin.read(1)

            # catch EOF
            if not from_console or from_console == '\x04':
                return False
            self.__chan.write(from_console)

        # TODO detect conn end
        return True

