# Reach, the remote acccess tool
# Copyright (C) 2010  Simon Poirier <simpoir@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

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

