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


    def called (self, command):
        """
            raises an exception when no more recorded calls are available or
            when the current recorded call does not have the expected command
            attribute, otherwise it will return the execution and remove the
            current recorded call from the list of recorded calls.
        """
    
        if not self.recorded_calls:
            raise AssertionError('No more recorded calls when verifying'
                                 'command "%s" called.' % command)
        
        actual_recorded_call = self.recorded_calls[0]
        if actual_recorded_call.command != command:
            raise AssertionError('Recorded call (execution) '
                                 'does not fulfill expectation:\n'
                                 'Expected command "%s", but got "%s"\n'
                                 % (command, actual_recorded_call.command))
        
        self.recorded_calls = self.recorded_calls[1:]
        return VerfiableExecutionWrapper(actual_recorded_call)
    
    
    def verify (self, command, arguments, stdin=None):
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


class VerfiableExecutionWrapper (object):
    """
        Verifier.called returns this wrapper to make a fluent interface
        possible.
    """
    
    
    def __init__ (self, execution):
        """
            stores the given execution and assures and_input = with_input.
        """
        
        self.execution = execution
        self.and_input = self.with_input


    def at_least_with_arguments (self, *expected_arguments):
        """
            raises a exception if the expeceted arguments are not in the
            arguments of the wrapped execution. Returns the wrapper itself
            to make invocation chaining possible.
        """
        
        arguments = list(expected_arguments)
        
        for argument in arguments:
            if argument not in self.execution.arguments:
                raise AssertionError(
                    'Stub "%s" has not been executed with at least '
                    'expected arguments %s, but with %s.'
                    % (self.execution.command, arguments, self.execution.arguments))
        
        return self


    def with_arguments (self, *expected_arguments):
        """
            raises a exception if the arguments of the wrapped execution are
            different than the expected arguments. Returns the wrapper itself
            to make invocation chaining possible.
        """
        
        arguments = list(expected_arguments)
        
        if self.execution.arguments != arguments:
            raise AssertionError(
                'Stub "%s" has not been executed with '
                'expected arguments %s, but with %s.'
                % (self.execution.command, arguments, self.execution.arguments))
        
        return self


    def with_input (self, expected_stdin):
        """
            raises a exception if the input from stdin in the wrapped execution
            is different than the expected stdin input. Returns the wrapper
            itself to make invocation chaining possible.
        """
        
        if self.execution.stdin != expected_stdin:
            raise AssertionError(
                'Stub "%s" has received the expected stdin '
                '"%s", but got "%s".'
                % (self.execution.command, expected_stdin, self.execution.stdin))
        
        return self

