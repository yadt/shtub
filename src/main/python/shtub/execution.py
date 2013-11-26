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

"""
    this module provides the class Execution, which represents a call to the
    command stub.
"""

__author__ = 'Alexander Metzner, Michael Gruber, Udo Juettner'

from shtub.commandinput import CommandInput


class Execution (object):

    """
        Represents the parameters of a call to the command stub.
    """

    def __init__(self, command, arguments, stdin, expected=False):
        """
            initializes a new execution with the given properties.
            If arguments is not given it will be initialized as empty list.
        """

        self.command_input = CommandInput(command, arguments, stdin)
        self.expected = expected

    def as_dictionary(self):
        """
            returns a dictionary representation of the execution.
        """

        return {'command_input': self.command_input.as_dictionary(),
                'expected': self.expected}

    def mark_as_expected(self):
        """
            marks the execution as expected which means the execution fulfills a stub configuration.
        """

        self.expected = True

    def __eq__(self, other):
        return self.command_input == other.command_input \
            and self.expected == other.expected

    def __ne__(self, other):
        return not(self == other)

    def __str__(self):
        """
            returns a string representation using as_dictionary.
        """

        return 'Execution %s' % (self.as_dictionary())

    @staticmethod
    def from_dictionary(dictionary):
        """
            returns a new execution object with the properties from the given
            dictionary.
        """

        command_input_dictionary = dictionary['command_input']

        return Execution(command_input_dictionary['command'],
                         command_input_dictionary['arguments'],
                         command_input_dictionary['stdin'],
                         dictionary['expected'])
