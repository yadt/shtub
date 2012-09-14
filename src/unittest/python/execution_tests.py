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

import unittest

from shtub.execution import Execution

class ExecutionTests (unittest.TestCase):
    def test_should_convert_dictionary_to_object (self):
        values = {'command_input': {'command'   : 'any_command',
                                    'arguments' : ['any_arguments'],
                                    'stdin'     : 'any_stdin'},
                  'expected'     : True}

        actual_execution = Execution.from_dictionary(values)

        self.assertEqual('any_command', actual_execution.command_input.command)
        self.assertEqual(['any_arguments'], actual_execution.command_input.arguments)
        self.assertEqual('any_stdin', actual_execution.command_input.stdin)
        self.assertEqual(True, actual_execution.expected)


    def test_should_create_object_with_given_properties (self):
        actual_execution = Execution('any_command', ['any_arg1', 'any_arg2'], 'any_stdin', expected=True)

        self.assertEqual('any_command', actual_execution.command_input.command)
        self.assertEqual(['any_arg1', 'any_arg2'], actual_execution.command_input.arguments)
        self.assertEqual('any_stdin', actual_execution.command_input.stdin)
        self.assertEqual(True, actual_execution.expected)


    def test_should_create_object_with_given_properties_but_empty_arguments (self):
        actual_execution = Execution('any_command', [], 'any_stdin')

        self.assertEqual('any_command', actual_execution.command_input.command)
        self.assertEqual([], actual_execution.command_input.arguments)
        self.assertEqual('any_stdin', actual_execution.command_input.stdin)
        self.assertEqual(False, actual_execution.expected)


    def test_should_convert_object_to_dictionary (self):
        execution = Execution('any_command', ['any_arg1', 'any_arg2'], 'any_stdin', expected=True)

        actual_dictionary = execution.as_dictionary()

        self.assertEqual('any_command', actual_dictionary['command_input']['command'])
        self.assertEqual(['any_arg1', 'any_arg2'], actual_dictionary['command_input']['arguments'])
        self.assertEqual('any_stdin', actual_dictionary['command_input']['stdin'])
        self.assertEqual(True, actual_dictionary['expected'])


    def test_should_return_false_when_objects_command_is_not_equal (self):
        execution1 = Execution('any_command', ['any_arg1', 'any_arg2'], 'any_stdin')
        execution2 = Execution('other_command', ['any_arg1', 'any_arg2'], 'any_stdin')

        self.assertFalse(execution1 == execution2, 'comparison of command')


    def test_should_return_false_when_objects_stdin_is_not_equal (self):
        execution1 = Execution('any_command', ['any_arg1', 'any_arg2'], 'any_stdin')
        execution2 = Execution('any_command', ['any_arg1', 'any_arg2'], 'other_stdin')

        self.assertFalse(execution1 == execution2, 'comparison of stdin')


    def test_should_return_false_when_objects_arguments_are_not_equal (self):
        execution1 = Execution('any_command', ['any_arg1', 'any_arg2'], 'any_stdin')
        execution2 = Execution('any_command', ['other_argument1', 'any_arg2'], 'any_stdin')

        self.assertFalse(execution1 == execution2, 'comparison of arguments')


    def test_should_return_true_when_objects_are_equal (self):
        execution1 = Execution('any_command', ['any_arg1', 'any_arg2'], 'any_stdin')
        execution2 = Execution('any_command', ['any_arg1', 'any_arg2'], 'any_stdin')

        self.assertTrue(execution1 == execution2, 'no difference, but not equal returned')


    def test_should_return_false_when_objects_are_equal_and_testing_if_not_equal (self):
        execution1 = Execution('any_command', ['any_arg1', 'any_arg2'], 'any_stdin')
        execution2 = Execution('any_command', ['any_arg1', 'any_arg2'], 'any_stdin')

        self.assertFalse(execution1 != execution2, 'no difference, but not equal returned')


    def test_should_return_true_when_objects_are_not_equal_and_testing_if_not_equal (self):
        execution1 = Execution('any_command', ['any_arg1', 'any_arg2'], 'any_stdin')
        execution2 = Execution('other_command', ['other_argument1', 'other_argument2'], 'other_stdin')

        self.assertTrue(execution1 != execution2, 'comparison: stdin')


    def test_should_return_false_when_one_object_is_not_fulfilled (self):
        execution1 = Execution('any_command', ['any_arg1', 'any_arg2'], 'any_stdin', expected=True)
        execution2 = Execution('any_command', ['any_arg1', 'any_arg2'], 'any_stdin')

        self.assertFalse(execution1 == execution2, 'comparison: stdin')


    def test_should_return_true_when_both_objects_are_fulfilled (self):
        execution1 = Execution('any_command', ['any_arg1', 'any_arg2'], 'any_stdin', expected=True)
        execution2 = Execution('any_command', ['any_arg1', 'any_arg2'], 'any_stdin', expected=True)

        self.assertTrue(execution1 == execution2, 'comparison: stdin')


    def test_should_return_string_with_all_properties (self):
        execution = Execution('any_command', ['any_arg1', 'any_arg2'], 'any_stdin')

        self.assertEqual("Execution {'expected': False, 'command_input': {'stdin': 'any_stdin', 'command': 'any_command', 'arguments': ['any_arg1', 'any_arg2']}}", str(execution))


    def test_should_mark_execution_as_fulfilled (self):
        execution = Execution('any_command', ['any_arg1', 'any_arg2'], 'any_stdin')

        execution.mark_as_expected()
        
        self.assertTrue(execution.expected)
