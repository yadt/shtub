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
from shtub import EXECUTIONS_FILENAME, deserialize_executions
from shtub.commandinput import CommandInput


class VerificationException (Exception):
    """
        to be raised when an error during verification occurs.
    """
    

class Verifier (object):
    """
        Verifies command stub expectations. Please use instances of this class
        in "with" statements.
    """
    
    def __init__ (self, basedir):
        """
            initializes a new verifier using the given base directory.
        """

        self.base_dir   = basedir
        self.executions = []


    def called (self, command):
        """
            raises an exception when no more executions are available or
            when the current execution does not have the expected command
            attribute, otherwise it will return the execution and remove the
            current execution from the list of executions.
        """
    
        if not self.executions:
            raise VerificationException('No more further executions: command "%s" can not be verified.' % command)
        
        actual_execution = self.executions[0]
        if actual_execution.command_input.command != command:
            raise VerificationException('Execution does not fulfill expectation:\n'
                                 'Expected command "%s", but got "%s"\n'
                                 % (command, actual_execution.command_input.command))
        
        self.executions = self.executions[1:]
        return VerfiableExecutionWrapper(actual_execution)
    
    
    def verify (self, command, arguments, stdin=None):
        """
            raises an exception when no more executions are available or
            when the current execution does not fulfill the given
            exception, otherwise it will pass and remove the current execution
            from the list of executions.
        """
    
        expected_input = CommandInput(command, arguments, stdin)

        if not self.executions:
            raise VerificationException('No more further executions, when verifying %s' % expected_input)
        
        actual_execution = self.executions[0]
        if not actual_execution.command_input.fulfills(expected_input):
            raise VerificationException('Execution does not fulfill expected_input:\n'
                                 'Expected %s\n'
                                 'Actual   %s\n'
                                 % (expected_input, actual_execution))
        
        self.executions = self.executions[1:]
    
    
    def __enter__ (self):
        """
            since this class is designed to be integrated in a "with" block it
            will load the actual executions and return itself.
        """
    
        filename = os.path.join(self.base_dir, EXECUTIONS_FILENAME)
        
        if not os.path.exists(filename):
            raise VerificationException('No executions found. Stubbed commands have never been called.')
    
        self.executions = deserialize_executions(filename)
        
        for execution in self.executions:
            if not execution.expected:
                raise VerificationException('Unexpected %s: did not fulfill any expectation.' % str(execution))
        
        return self


    def __exit__(self, exception_type, exception_value, traceback):
        """
            since this class is designed to be integrated in a "with" block it
            is implemented, but has no effect.

            @return: False, when exception_type, exception_value or traceback given,
                     otherwise None
        """
        
        if exception_type or exception_value or traceback:
            return False
        
        count_of_executions = len(self.executions)
        if count_of_executions > 0:
            if count_of_executions == 1:
                message = 'There is an unverified execution:\n'
            else:
                message = 'There are %s unverified executions:\n' % count_of_executions
                
            for execution in self.executions:
                message += "    %s\n" % str(execution)
                
            raise VerificationException(message)


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
            if argument not in self.execution.command_input.arguments:
                raise VerificationException(
                    'Stub "%s" has not been executed with at least expected arguments %s, but with %s.'
                    % (self.execution.command_input.command, arguments, self.execution.command_input.arguments))
        
        return self


    def with_arguments (self, *expected_arguments):
        """
            raises a exception if the arguments of the wrapped execution are
            different than the expected arguments. Returns the wrapper itself
            to make invocation chaining possible.
        """
        
        arguments = list(expected_arguments)
        
        if self.execution.command_input.arguments != arguments:
            raise VerificationException(
                'Stub "%s" has not been executed with expected arguments %s, but with %s.'
                % (self.execution.command_input.command, arguments, self.execution.command_input.arguments))
        
        return self


    def with_input (self, expected_stdin):
        """
            raises a exception if the input from stdin in the wrapped execution
            is different than the expected stdin input. Returns the wrapper
            itself to make invocation chaining possible.
        """
        
        if self.execution.command_input.stdin != expected_stdin:
            raise VerificationException(
                'Stub "%s" has not received the expected stdin "%s", but got "%s".'
                % (self.execution.command_input.command, expected_stdin, self.execution.command_input.stdin))
        
        return self
