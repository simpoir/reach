import os

class Completor:
    def fill(self, host, requested):
        """ Completes the host structure to the best of this completor's
        knowledge.

        host a dictionary of host string attributes
        requested a tuple of required connection attributes

        A completor may not fill anything if the host is unknown or if
        known attributes are already filled. A completor shall not,
        however overwrite an already filled parameter, if it doesn't match
        its values.
        Required attributes are "necessary" attribute names, that will
        have to be completed by one of the many defined Completors.
        A Completor may use it for lookup or ignore it and simply fill
        all known values.
        """
        raise NotImplementedError()

    def lookup(self, host):
        """ Returns a list of host that can see the specified host.
        Visibility lookup can be done from the host scope attribute.

        If lookup fails an empty list should be returned
        """
        raise NotImplementedError()

default_chain = ('config', 'interactive')

registry = {}

def load_completors():
    """ Load all completors modules located in the reach.completors package.

        Completors are expected to insert themselves to the registry.
    """
    registry.clear()
    complnames = os.listdir(os.path.dirname(__file__) + 'completors')
    for complname in complnames:
        if (not complname.endswith('.py')) or (complname[0] == '_'):
            continue
        compl_mod_name = complname.rpartition('.')[0]
        compl_mod = __import__('reach.completors.'+compl_mod_name, fromlist=[True])

def init_completors(settings):
    chain_names = default_chain + settings.get_completor_chain()

    chain = []
    for completor_name in chain_names:
        chain.append(registry[completor_name]())

    return chain

