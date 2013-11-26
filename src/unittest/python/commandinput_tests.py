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

from shtub.commandinput import CommandInput


class CommandInputTests (unittest.TestCase):

    def test_should_convert_dictionary_to_object(self):
        values = {'command': 'any_command',
                  'arguments': ['any_arguments'],
                  'stdin': 'any_stdin'}

        actual = CommandInput.from_dictionary(values)

        self.assertEqual(
            CommandInput('any_command', ['any_arguments'], 'any_stdin'), actual)

    def test_should_create_object_with_given_properties(self):
        actual = CommandInput(
            'any_command', ['any_arg1', 'any_arg2'], 'any_stdin')

        self.assertEqual('any_command', actual.command)
        self.assertEqual(['any_arg1', 'any_arg2'], actual.arguments)
        self.assertEqual('any_stdin', actual.stdin)

    def test_should_create_object_with_given_properties_but_empty_arguments(self):
        actual = CommandInput('any_command', [], 'any_stdin')

        self.assertEqual('any_command', actual.command)
        self.assertEqual([], actual.arguments)
        self.assertEqual('any_stdin', actual.stdin)

    def test_should_convert_object_to_dictionary(self):
        command_input = CommandInput(
            'any_command', ['any_arg1', 'any_arg2'], 'any_stdin')

        actual_dictionary = command_input.as_dictionary()

        expected_dictionary = {'command': 'any_command',
                               'arguments': ['any_arg1', 'any_arg2'],
                               'stdin': 'any_stdin'}
        self.assertEqual(expected_dictionary, actual_dictionary)

    def test_should_return_false_when_objects_command_is_not_equal(self):
        command_input1 = CommandInput(
            'any_command', ['any_arg1', 'any_arg2'], 'any_stdin')
        command_input2 = CommandInput(
            'other_command', ['any_arg1', 'any_arg2'], 'any_stdin')

        self.assertFalse(
            command_input1 == command_input2, 'comparison of command')

    def test_should_return_true_when_stdin_is_none(self):
        command_input1 = CommandInput('any_command', ['argument'], 'any_stdin')
        command_input2 = CommandInput('any_command', ['argument'], None)

        self.assertTrue(command_input1.fulfills(command_input2))

    def test_should_return_false_when_objects_stdin_is_not_equal(self):
        command_input1 = CommandInput(
            'any_command', ['any_arg1', 'any_arg2'], 'any_stdin')
        command_input2 = CommandInput(
            'any_command', ['any_arg1', 'any_arg2'], 'other_stdin')

        self.assertFalse(
            command_input1 == command_input2, 'comparison of stdin')

    def test_should_return_false_when_objects_arguments_are_not_equal(self):
        command_input1 = CommandInput(
            'any_command', ['any_arg1', 'any_arg2'], 'any_stdin')
        command_input2 = CommandInput(
            'any_command', ['other_argument1', 'any_arg2'], 'any_stdin')

        self.assertFalse(
            command_input1 == command_input2, 'comparison of arguments')

    def test_should_return_true_when_objects_are_equal(self):
        command_input1 = CommandInput(
            'any_command', ['any_arg1', 'any_arg2'], 'any_stdin')
        command_input2 = CommandInput(
            'any_command', ['any_arg1', 'any_arg2'], 'any_stdin')

        self.assertTrue(command_input1 == command_input2,
                        'no difference, but not equal returned')

    def test_should_return_false_when_objects_are_equal_and_testing_if_not_equal(self):
        command_input1 = CommandInput(
            'any_command', ['any_arg1', 'any_arg2'], 'any_stdin')
        command_input2 = CommandInput(
            'any_command', ['any_arg1', 'any_arg2'], 'any_stdin')

        self.assertFalse(
            command_input1 != command_input2, 'no difference, but not equal returned')

    def test_should_return_true_when_objects_are_not_equal_and_testing_if_not_equal(self):
        command_input1 = CommandInput(
            'any_command', ['any_arg1', 'any_arg2'], 'any_stdin')
        command_input2 = CommandInput(
            'other_command', ['other_argument1', 'other_argument2'], 'other_stdin')

        self.assertTrue(command_input1 != command_input2, 'comparison: stdin')

    def test_should_return_string_with_all_properties(self):
        given_object = CommandInput(
            'any_command', ['any_arg1', 'any_arg2'], 'any_stdin')

        actual_string = str(given_object)

        self.assertEqual(
            "CommandInput {'stdin': 'any_stdin', 'command': 'any_command', 'arguments': ['any_arg1', 'any_arg2']}", actual_string)

    def test_should_return_false_if_other_has_different_arguments(self):
        command_input1 = CommandInput(
            'any_command', ['any_arg1', 'any_arg2'], 'any_stdin')
        command_input2 = CommandInput(
            'any_command', ['other_argument1', 'other_argument2'], 'any_stdin')

        self.assertFalse(command_input1.fulfills(command_input2))

    def test_should_return_false_if_other_has_at_least_one_different_argument(self):
        command_input1 = CommandInput(
            'any_command', ['any_arg1', 'any_arg2'], 'any_stdin')
        command_input2 = CommandInput(
            'any_command', ['any_arg1', 'any_arg2', 'other_argument'], 'any_stdin')

        self.assertFalse(command_input1.fulfills(command_input2))

    def test_should_return_true_if_other_has_no_arguments(self):
        command_input1 = CommandInput(
            'any_command', ['any_arg1', 'any_arg2'], 'any_stdin')
        command_input2 = CommandInput('any_command', [], 'any_stdin')

        self.assertTrue(command_input1.fulfills(command_input2))

    def test_should_return_true_if_other_has_exactly_one_matching_argument_and_no_others(self):
        command_input1 = CommandInput(
            'any_command', ['any_arg1', 'any_arg2'], 'any_stdin')
        command_input2 = CommandInput('any_command', ['any_arg1'], 'any_stdin')

        self.assertTrue(command_input1.fulfills(command_input2))

    def test_should_return_true_if_other_has_equal_arguments(self):
        command_input1 = CommandInput(
            'any_command', ['any_arg1', 'any_arg2'], 'any_stdin')
        command_input2 = CommandInput(
            'any_command', ['any_arg2', 'any_arg1'], 'any_stdin')

        self.assertTrue(command_input1.fulfills(command_input2))

    def test_should_return_false_when_other_has_different_command_but_equal_arguments(self):
        command_input1 = CommandInput(
            'any_command', ['any_arg1', 'any_arg2'], 'any_stdin')
        command_input2 = CommandInput(
            'other_command', ['any_arg2', 'any_arg1'], 'any_stdin')

        self.assertFalse(command_input1.fulfills(
            command_input2), 'comparison: command')

    def test_should_return_false_when_other_has_different_stdin(self):
        command_input1 = CommandInput(
            'any_command', ['any_arg1', 'any_arg2'], 'any_stdin')
        command_input2 = CommandInput(
            'any_command', ['any_arg1', 'any_arg2'], 'other_stdin')

        self.assertFalse(
            command_input1.fulfills(command_input2), 'comparison: stdin')

    def test_should_return_true_when_other_equal_command_and_arguments(self):
        command_input1 = CommandInput(
            'any_command', ['any_arg1', 'any_arg2'], 'any_stdin')
        command_input2 = CommandInput(
            'any_command', ['any_arg2', 'any_arg1'], 'any_stdin')

        self.assertTrue(command_input1.fulfills(
            command_input2), 'comparison: command')
