from reach import completor

import pexpect
import os

class SshConnector(object):
    # basic required args
    required = ('hostname', 'port', 'username')

    # default completion mapping
    defaults = (('port', '22'),
                ('username', os.environ.get('USER')))

    class __default_completor(completor.Completor):
        def fill(self, host, requested):
            for parm,val in SshConnector.defaults:
                if not host.get(parm, False):
                    host[parm] = val

        def lookup(self, host):
            return []


    def connect(self, host, channel):
        """ Connect to host using channel as spawn shell.

        This will be called recursively on a channel.
        """
        #print("i would connect to %(hostname)s on port %(port)s with user %(username)s and password %(password)s"%host)
        #raise NotImplementedError()

        chan = channel.get_io()
        chan.timeout = 2
        chan.write('ssh -o ControlPath=none -p %(port)s %(username)s@%(hostname)s\n'%host)
        chan.expect('assword')
        chan.write(host['password']+'\n')

        chan.write('echo REACH ROCKS')
        chan.expect('REACH ROCKS') # flush untill the echo
        chan.write('\n')

        try:
            chan.expect('REACH ROCKS')
        except pexpect.TIMEOUT, e:
            # TODO get cause
            print('connection to %(username)s@%(hostname)s failed'%host)
            raise e
        print('succeeded connnecting to %s'%host['hostname'])

    def get_required(self, host):
        """ Returns a list of required host attributes to connect to host.

        Returned attributes may be already assigned in host.
        """
        if host.has_key('sshkey') and host.get('sshkey') != None:
            return SshConnector.required + ('sshkey',)

        return SshConnector.required + ('password',)


    def get_defaults_completor(self):
        """ Returns a Completor object for this connector's defaults.
        """
        return SshConnector.__default_completor()

