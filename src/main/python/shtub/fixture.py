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

"""
    this module provides the class Fixture, which represents the test fixture,
    e.g. it offers methods to create expectations for the command stub. 
"""

__author__ = 'Alexander Metzner, Michael Gruber, Udo Juettner'

import os

from shtub import EXPECTATIONS_FILENAME, serialize_executions
from shtub.expectation import Expectation

class Fixture (object):
    """
        Represents the testing context which can be configured by defining
        expectations and corresponding answers. Please use instances of this
        class in a "with" statement.
    """
    
    def __init__ (self, basedir):
        """
            initializes a new fixture with the given base directory.
        """
        
        self.base_dir     = basedir
        self.expectations = []
    
    # quickfix: expecting empty string instead of None, to make sure there's no difference
    #           between execution within tty and without
    def expect (self, command, arguments, stdin=''):
        """
            creates a new expectation with the given properties and appends it
            to the expectations, then returns the expectation for invocation
            chaining.
        """
        
        expectation = Expectation(command, arguments, stdin)
        self.expectations.append(expectation)
        
        return expectation
    
    
    def calling (self, command):
        """
            creates a new expecation with the given command and appends it to
            the expectations, then returns the expecation for invocation
            chaining.
        """
    
        expectation = Expectation(command)
        self.expectations.append(expectation)
        
        return expectation

    
    def __enter__ (self):
        """
            since this class is designed to be used using the "with" statement
            this returns the fixture itself.
        """
        
        return self
    
    
    def __exit__ (self, exception_type, exception_value, traceback):
        """
            since this class is designed to be used using the "with" statement
            this will save the list of expectations in the base directory.
            
            @return: False, when exception_type, exception_value or traceback given,
                     otherwise None
        """
         
        if exception_type or exception_value or traceback:
            return False
               
        filename = os.path.join(self.base_dir, EXPECTATIONS_FILENAME)
        
        serialize_executions(filename, self.expectations)
