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

import unittest

from mock import patch, call

from shtub.fixture import Fixture


class FixtureTest (unittest.TestCase):
    def test_should_create_object_with_given_base_dir_and_empty_list_of_stub_configurations(self):
        actual = Fixture('/abc/def')

        self.assertEqual('/abc/def', actual.base_directory)
        self.assertEqual([], actual.stub_configurations)


    def test_should_append_a_new_stub_configuration(self):
        fixture = Fixture('/test123')
        fixture.calling('any_command').at_least_with_arguments('any_arg0', 'any_arg1', 'any_arg2').and_input('any_stdin')

        actual_stub_configurations = fixture.stub_configurations
        
        self.assertEqual(1, len(actual_stub_configurations))

        actual_stub_configuration = actual_stub_configurations[0]

        self.assertEqual('any_command', actual_stub_configuration.command_input.command)
        self.assertEqual(['any_arg0', 'any_arg1', 'any_arg2'], actual_stub_configuration.command_input.arguments)
        self.assertEqual('any_stdin', actual_stub_configuration.command_input.stdin)


    def test_should_append_a_new_stub_configuration_with_default_stdin_and_arguments(self):
        fixture = Fixture('/test123')

        actual_return_value = fixture.calling('any_command')
        
        actual_stub_configurations = fixture.stub_configurations
        self.assertEqual(1, len(actual_stub_configurations))

        actual_stub_configuration = actual_stub_configurations[0]

        self.assertEqual(actual_return_value, actual_stub_configuration)
        self.assertEqual('any_command', actual_stub_configuration.command_input.command)
        self.assertEqual([], actual_stub_configuration.command_input.arguments)
        self.assertEqual(None, actual_stub_configuration.command_input.stdin)


    @patch('shtub.fixture.serialize_executions')
    def test_should_return_fixture_itself_when_entering_with_statement_and_serialize_stub_configurations_when_exiting (self, serialize_mock):
        fixture = Fixture('/hello/world')

        with fixture as fix:
            self.assertEqual(fix, fixture)

        self.assertEqual(call('/hello/world/shtub/stub-configurations', []), serialize_mock.call_args)


    def test_should_not_suppress_exceptions (self):
        fixture = Fixture('/spam/eggs')
        
        actual_result = fixture.__exit__('exception_type', 'exception_value', 'traceback')

        self.assertFalse(actual_result)
