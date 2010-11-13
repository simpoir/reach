#!/usr/bin/env python
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

from distutils.core import setup

from reach import VERSION_MAJOR, VERSION_MINOR, VERSION_REVISION

setup(name='reach',
      version='%d.%d.%d'%(VERSION_MAJOR, VERSION_MINOR, VERSION_REVISION),
      author='Simon Poirier',
      author_email='simpoir@gmail.com',
      url='http://github.com/simpoir/reach/',
      packages=['reach', 'reach.commands', 'reach.completors'],
      scripts=['r2'],
     )


