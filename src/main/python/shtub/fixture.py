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
    this module provides the class Fixture, which represents the test fixture,
    e.g. it offers methods to configure the command stub.
"""

__author__ = 'Alexander Metzner, Michael Gruber, Udo Juettner'

import os

from shtub import CONFIGURED_STUBS_FILENAME, serialize_as_dictionaries
from shtub.stubconfiguration import StubConfiguration


class Fixture (object):

    """
        Represents the testing context which contains stub configurations and corresponding answers.
        Please use instances of this class in a "with" statement.
    """

    def __init__(self, base_directory):
        """
            initializes a new fixture with the given base directory.
        """

        self.base_directory = base_directory
        self.stub_configurations = []

    def calling(self, command):
        """
            creates a new StubConfiguration with the given command and appends it to
            the stub_configurations, then returns the stub_configuration for invocation
            chaining.
        """
        stub_configuration = StubConfiguration(command)
        self.stub_configurations.append(stub_configuration)

        return stub_configuration

    def __enter__(self):
        """
            since this class is designed to be used using the "with" statement
            this returns the fixture itself.
        """
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        """
            since this class is designed to be used in a "with" statement
            this will save the list of stub_configurations in the base directory.

            @return: False, when exception_type, exception_value or traceback given,
                     otherwise None
        """

        if exception_type or exception_value or traceback:
            return False

        filename = os.path.join(self.base_directory, CONFIGURED_STUBS_FILENAME)

        serialize_as_dictionaries(filename, self.stub_configurations)
