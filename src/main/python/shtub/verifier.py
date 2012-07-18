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

import os.path
from shtub import RECORDED_CALLS_FILENAME, deserialize_stub_executions
from shtub.execution import Execution


class Verifier (object):
    def __init__ (self, basedir):
        self.base_dir       = basedir
        self.recorded_calls = []

    def verify (self, command, arguments, stdin):
        expectation = Execution(command, arguments, stdin)

        if not self.recorded_calls:
            raise AssertionError('No more recorded calls when verifying %s'
                                 % expectation)
        
        if not self.recorded_calls[0].fulfills(expectation):
            raise AssertionError('Recorded call (execution) '
                                 'does not fulfill expectation:\n'
                                 'Expected %s\n'
                                 'Actual   %s\n'
                                 % (expectation, self.recorded_calls[0]))
        
        self.recorded_calls = self.recorded_calls[1:]
    
    def __enter__ (self):
        filename = os.path.join(self.base_dir, RECORDED_CALLS_FILENAME)
        self.recorded_calls = deserialize_stub_executions(filename)
        return self
    
    def __exit__(self, exception_type, exception_value, traceback):
        pass
