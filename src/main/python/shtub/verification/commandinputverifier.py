#   shtub - shell command stub
#   Copyright (C) 2012-2013 Immobilien Scout GmbH
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

__author__ = 'Alexander Metzner, Michael Gruber, Udo Juettner, Maximilien Riehl, Marcel Wolf'

import re
from shtub.verification import VerificationException


class CommandInputVerifier (object):
    """
        VerifierLoader.called returns this wrapper to make a fluent interface
        possible.
    """

    def __init__(self, command_input):
        """
            stores command, arguments and stdin and assures
            and_input = with_input,
            and_at_least_one_argument_matches = at_least_one_argument_matches
        """
        self.command = command_input.command
        self.arguments = command_input.arguments
        self.stdin = command_input.stdin

        self.and_input = self.with_input
        self.and_at_least_one_argument_matches = self.at_least_one_argument_matches


    def at_least_with_arguments(self, *expected_arguments):
        """
            raises an exception if the expeceted arguments are not in the
            arguments of the wrapped execution. Returns the wrapper itself
            to make invocation chaining possible.
        """
        arguments = list(expected_arguments)

        for argument in arguments:
            if argument not in self.arguments:
                raise VerificationException(
                    'Stub "%s" has not been executed with at least expected arguments %s, but with %s.'
                    % (self.command, arguments, self.arguments))

        return self


    def with_arguments(self, *expected_arguments):
        """
            raises an exception if the arguments of the wrapped execution are
            different than the expected arguments. Returns the wrapper itself
            to make invocation chaining possible.
        """
        arguments = list(expected_arguments)

        if self.arguments != arguments:
            raise VerificationException(
                'Stub "%s" has not been executed with expected arguments %s, but with %s.'
                % (self.command, arguments, self.arguments))

        return self


    def with_input(self, expected_stdin):
        """
            raises an exception if the input from stdin in the wrapped execution
            is different than the expected stdin input. Returns the wrapper
            itself to make invocation chaining possible.
        """
        if self.stdin != expected_stdin:
            raise VerificationException(
                'Stub "%s" has not received the expected stdin "%s", but got "%s".'
                % (self.command, expected_stdin, self.stdin))

        return self


    def at_least_one_argument_matches(self, pattern):
        """
            raises an exception if none of the arguments matches the given pattern.
        """
        compiled_pattern = re.compile(pattern)

        for argument in self.arguments:
            if compiled_pattern.match(argument):
                return self

        raise VerificationException(
            'Stub "{0}" has not been executed with at least one argument matching pattern "{1}",\ngot arguments {2}' \
                .format(self.command, pattern, self.arguments))
