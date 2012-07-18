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

import os

from shtub import BASEDIR, serialize_stub_executions
from shtub.expectation import Expectation

class Fixture (object):
    def __init__ (self, basedir):
        self.base_dir     = basedir
        self.expectations = []
        
    def expect (self, command, arguments, stdin):
        expectation = Expectation(command, arguments, stdin)
        self.expectations.append(expectation)
        
        return expectation
    
    def __enter__ (self):
        return self
    
    def __exit__ (self, exception_type, exception_value, traceback):
        __pychecker__ = 'unusednames=exception_type,exception_value,traceback'
        filename = os.path.join(self.base_dir, BASEDIR, 'expectations')
        
        serialize_stub_executions(filename, self.expectations)
