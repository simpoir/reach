from reach import sshconnector

class Channel(object):
    """ Represents a channel, I.E. a IO stream to a shell or something
    that is at least interactive enough for SshConnector to do something with.
    """
    pass

    def chain_connect(self, chain):
        conn = sshconnector.SshConnector()

        for link in chain:
            conn.connect(link, self)

    def run(self):
        # TODO pass data between stdin -> channel, channel -> stdout
        return False

