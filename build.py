#   shtub - shell command stub
#   Copyright (C) 2012 Immobilien Scout GmbH
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
from pythonbuilder.core import use_plugin, init, Author

use_plugin('filter_resources')

use_plugin('python.core')
use_plugin('python.coverage')
use_plugin('python.unittest')
use_plugin('python.integrationtest')
use_plugin('python.install_dependencies')
use_plugin('python.distutils')
use_plugin('python.pychecker')
use_plugin('python.pydev')

name    = 'shtub'
authors = [Author('Alexander Metzner', 'alexander.metzner@gmail.com'),
           Author('Michael Gruber', 'aelgru@gmail.com'),
           Author('Udo Juettner', 'udo.juettner@gmail.com')]
license = 'GNU GPL v3'
summary = 'shtub - shell command stub'
url     = 'https://github.com/yadt/shtub'
version = '0.2.7'

default_task = ['install_dependencies', 'analyze', 'publish']


def is_python_version(expected_major, expected_minor):
    major, minor, micro, releaselevel, serial = sys.version_info
    return major == expected_major and minor == expected_minor
        
@init
def set_properties (project):
    project.build_depends_on('coverage')
    project.build_depends_on('mock')
    
    if is_python_version(2, 6):
        project.build_depends_on('unittest2')
        
    project.set_property('coverage_break_build', True)
    project.get_property('coverage_exceptions').append('shtub.testbase')

    project.set_property('pychecker_break_build', True)
    project.set_property('pychecker_args', ['-Q', '-b', 'unittest'])

    project.get_property('distutils_commands').append('bdist_egg')
    project.get_property('distutils_commands').append('bdist_rpm')

    project.get_property('filter_resources_glob').append('**/shtub/__init__.py')
