from reach import completor

class ComplConfig(completor.Completor):
    def fill(self, host, requested):
        # TODO
        raise NotImplementedError()

    def lookup(self, scope):
        # TODO
        raise NotImplementedError()

completor.registry.update('config', ComplConfig)

