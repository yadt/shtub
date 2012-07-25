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
    this module provides the class Verifier which offers methods to verify if
    the command stub has been called in the expected way. 
"""

__author__ = 'Alexander Metzner, Michael Gruber, Udo Juettner'

import os.path
from shtub import RECORDED_CALLS_FILENAME, deserialize_executions
from shtub.execution import Execution


class Verifier (object):
    """
        Verifies command stub expectations. Please use instances of this class
        in "with" statements.
    """
    
    def __init__ (self, basedir):
        """
            initializes a new verifier using the given base directory.
        """

        self.base_dir       = basedir
        self.recorded_calls = []


    def verify (self, command, arguments, stdin):
        """
            raises an exception when no more recorded calls are available or
            when the current recorded call does not fulfill the given
            exception, otherwise it will pass and remove the current recorded
            call from the list of recorded calls.
        """
    
        expectation = Execution(command, arguments, stdin)

        if not self.recorded_calls:
            raise AssertionError('No more recorded calls when verifying %s'
                                 % expectation)
        
        actual_recorded_call = self.recorded_calls[0]
        if not actual_recorded_call.fulfills(expectation):
            raise AssertionError('Recorded call (execution) '
                                 'does not fulfill expectation:\n'
                                 'Expected %s\n'
                                 'Actual   %s\n'
                                 % (expectation, actual_recorded_call))
        
        self.recorded_calls = self.recorded_calls[1:]
    
    
    def __enter__ (self):
        """
            since this class is designed to be integrated in a "with" block it
            will load the actual recorded calls and return itself.
        """
    
        filename = os.path.join(self.base_dir, RECORDED_CALLS_FILENAME)
        self.recorded_calls = deserialize_executions(filename)
        return self


    def __exit__(self, exception_type, exception_value, traceback):
        """
            since this class is designed to be integrated in a "with" block it
            is implemented, but has no effect.
        """
        
        pass
