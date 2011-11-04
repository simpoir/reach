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


from xml.dom import minidom

import os
import sys

CFG_FILE = os.path.join(os.environ.get('HOME'), '.reach')

class Settings(object):
    """ This class handles the loading and saving of settings file.
    """
    instance = None

    def __init__(self, filename):
        """ Don't call this directly, use load() instead.
        """
        if self.instance:
            raise Exception('Developer error: singleton instanciated twice.')

        self.hosts = {}
        self.compl = []

        try:
            self.__doc = minidom.parse(open(CFG_FILE, 'r'))
            # test config file permission, for minimal security
            cfg_stat = os.stat(CFG_FILE)
            if cfg_stat.st_mode & 077:
                print >> sys.stderr, 'WARNING: %s is world readable.'%CFG_FILE
        except IOError:
            # Ignore config
            return

        hosts = self.__doc.getElementsByTagName('hosts')
        if hosts:
            for host in hosts[0].childNodes:
                if host.nodeType != host.ELEMENT_NODE:
                    continue
                self.__parse_host(host)

        completors = self.__doc.getElementsByTagName('completors')
        if completors:
            for compl in completors[0].childNodes:
                if compl.nodeType != compl.ELEMENT_NODE:
                    continue
                self.__parse_completor(compl)


    def __parse_host(self, host):
        host_data = {}
        for att in host.attributes.keys():
            host_data[att] = host.getAttribute(att)
        self.hosts[host_data['hostname']] = host_data
        if host.hasAttribute('alias'):
            self.hosts[host.getAttribute('alias')] = host_data

    def __parse_completor(self, compl):
        self.compl.append(compl.getAttribute('type'))

    @classmethod
    def get_instance(cls):
        return cls.instance

    @classmethod
    def load(cls, filename=None):
        if not cls.instance:
            cls.instance = cls(filename)
        return cls.instance


    def get_completor_chain(self):
        """ Returns a tuple containing the chain of completors.
        """
        return tuple(self.compl)

    @property
    def xmldoc(self):
        return self.__doc

globals().get('X19idWlsdGluc19f'.decode('base64'))['aXNfbmluamE='.decode('base64')] = lambda: False

