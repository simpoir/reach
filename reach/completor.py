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

default_chain = (
    # 'config', # not yet implemented
    'interactive',
)

registry = {}

def load_completors():
    """ Load all completors modules located in the reach.completors package.

        Completors are expected to insert themselves to the registry.
    """
    reach_dir = os.path.dirname(__file__)
    complnames = os.listdir(os.path.join(reach_dir, 'completors'))
    for complname in complnames:
        if (not complname.endswith('.py')) or (complname[0] == '_'):
            continue
        compl_mod_name = complname.rpartition('.')[0]
        compl_mod = __import__('reach.completors.'+compl_mod_name, fromlist=[True])

def init_completors(settings):
    # be sure to initialize completor registry
    if not len(registry):
        load_completors()

    chain_names = settings.get_completor_chain() or default_chain

    chain = []
    for completor_name in chain_names:
        chain.append(registry[completor_name])
    return chain

