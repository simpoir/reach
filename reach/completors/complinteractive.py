from reach import completor

import getpass


ASK_RESOLUTION = False

class ComplInteractive(completor.Completor):
    def fill(self, host, requested):
        """ Spam user about requested params. The rest doesn't matter.
        """

        # FIXME I don't see a backend without a hostname, but I don't like
        # direct depenencies to host attributes.
        host_name = host.get('hostname', 'unknown host name')

        for req_name in requested:
            if (not host.has_key(req_name)) or (host.get(req_name) == None):
                if req_name == 'password':
                    val = getpass.getpass("'%s' %s: " % (host_name, req_name))
                else:
                    val = raw_input("'%s' %s: " % (host_name, req_name))
                host[req_name] = val

    def lookup(self, host):
        """ Does not lookup anything; user already completed using the sys.argv
        """
        return []

completor.registry['interactive'] = ComplInteractive()

