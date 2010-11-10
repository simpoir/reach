from reach import completor
from reach import host as host_constants

ASK_RESOLUTION = False

class ComplInteractive(completor.Completor):
    def fill(self, host, requested):
        """ Spam user about requested params. The rest doesn't matter.
        """
        for req_name in requested:
            print("'%s' parameters:" % host[host_constants.HOSTNAME])
            if (not host.has_key(req_name)) or (host.get(req_name) == None):
                val = raw_input("    %s: " % req_name)
                host.update(req_name, val)

    def lookup(self, host):
        """ Does not lookup anything; user already completed using the sys.argv
        """
        return []

completor.registry.update('interactive', ComplInteractive)

