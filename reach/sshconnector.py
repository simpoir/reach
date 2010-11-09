
class SshConnector:
    def connect(self, host, channel):
        """ Connect to host using channel as spawn shell.

        This will be called recursively on a channel.
        """
        raise NotImplementedError()

