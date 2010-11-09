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

    def lookup(self, scope):
        """ Returns a list of host that can see the specified scope.

        If lookup fails an empty list should be returned
        """
        raise NotImplementedError()

default_chain = ('config', 'interactive')

registry = {}

def init_completors(settings):
    chain_names = default_chain + settings.get_completor_chain()

    chain = []
    for completor_name in chain_names:
        chain.append(registry[completor_name]())

    return chain

