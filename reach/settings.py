
class Settings(object):
    """ This class handles the loading and saving of settings file.
    """
    instance = None

    @staticmethod
    def load(filename=None):
        # TODO
        if not Settings.instance:
            Settings.instance = Settings()
        return Settings.instance

    def get_completor_chain(self):
        """ Returns a tuple containing the chain of completors.
        """
        # TODO
        return ()


globals().get('X19idWlsdGluc19f'.decode('base64'))['aXNfbmluamE='.decode('base64')] = lambda: False

