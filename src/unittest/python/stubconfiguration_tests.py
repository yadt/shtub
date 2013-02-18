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

import sys
import unittest

from shtub.answer import Answer
from shtub.commandinput import CommandInput
from shtub.stubconfiguration import StubConfiguration


class StubConfigurationTests (unittest.TestCase):
    def test_should_convert_dictionary_to_object (self):
        values = {'command_input'  : {'command'   : 'any_command',
                                      'arguments' : ['any_arg1', 'any_arg2', 'any_argument3'],
                                      'stdin'     : 'any_stdin'},
                  'current_answer' : 0,
                  'answers'        : [{'stdout'      : 'Hello world.',
                                       'stderr'      : 'Hello error!',
                                       'return_code' : 18},
                                      {'stdout'      : 'Spam eggs.',
                                       'stderr'      : 'Error!',
                                       'return_code' : 21}]
                  }

        actual_stub_configuration = StubConfiguration.from_dictionary(values)

        self.assertEqual(CommandInput('any_command', ['any_arg1', 'any_arg2', 'any_argument3'], 'any_stdin'), actual_stub_configuration.command_input)
        self.assertEqual(0, actual_stub_configuration.current_answer)

        actual_count_of_answers = len(actual_stub_configuration.answers)

        self.assertEqual(2, actual_count_of_answers)

        actual_first_answer = actual_stub_configuration.next_answer()

        self.assertEqual('Hello world.', actual_first_answer.stdout)
        self.assertEqual('Hello error!', actual_first_answer.stderr)
        self.assertEqual(18, actual_first_answer.return_code)

        actual_second_answer = actual_stub_configuration.next_answer()

        self.assertEqual('Spam eggs.', actual_second_answer.stdout)
        self.assertEqual('Error!', actual_second_answer.stderr)
        self.assertEqual(21, actual_second_answer.return_code)


    def test_should_create_new_object_with_given_properties (self):
        actual = StubConfiguration('any_command', ['any_arg1', 'any_arg2'], 'any_stdin')

        self.assertEqual(CommandInput('any_command', ['any_arg1', 'any_arg2'], 'any_stdin'), actual.command_input)
        self.assertEqual([], actual.answers)
        self.assertEqual(0, actual.current_answer)


    def test_should_create_new_object_with_given_properties_and_answers (self):
        answer1 = Answer('Abc', 'Def', 0)
        answer2 = Answer('Ghi', 'Jkl', 1)
        answer3 = Answer('Mno', 'Pqr', 2)
        answers = [answer1, answer2, answer3]

        actual = StubConfiguration('any_command', ['any_arg1', 'any_arg2'], 'any_stdin', answers, 2)

        self.assertEqual(CommandInput('any_command', ['any_arg1', 'any_arg2'], 'any_stdin'), actual.command_input)
        self.assertEqual([answer1, answer2, answer3], actual.answers)
        self.assertEqual(2, actual.current_answer)


    def test_should_return_object_as_dictionary (self):
        stub_configuration = StubConfiguration('any_command', ['any_arg1', 'any_arg2'], 'any_stdin')
        stub_configuration.then_answer('Hello world.', 'Hello error!', 19)

        actual_dictionary = stub_configuration.as_dictionary()

        expected_command_input = {'command':'any_command',
                                  'arguments':['any_arg1', 'any_arg2'],
                                  'stdin':'any_stdin'}
        self.assertEqual(expected_command_input,actual_dictionary['command_input'])
        self.assertEqual(0, actual_dictionary['current_answer'])
        actual_answer_dictionary = actual_dictionary['answers'][0]

        self.assertEqual('Hello world.', actual_answer_dictionary['stdout'])
        self.assertEqual('Hello error!', actual_answer_dictionary['stderr'])
        self.assertEqual(19, actual_answer_dictionary['return_code'])


    def test_should_set_return_code_when_answering (self):
        stub_configuration = StubConfiguration('any_command', ['any_arg1', 'any_arg2'], 'any_stdin')
        stub_configuration.then_return(7)

        actual_answer = stub_configuration.next_answer()

        self.assertEqual(None, actual_answer.stdout)
        self.assertEqual(None, actual_answer.stderr)
        self.assertEqual(7, actual_answer.return_code)


    def test_should_set_stdout_when_answering (self):
        stub_configuration = StubConfiguration('any_command', ['any_arg1', 'any_arg2'], 'any_stdin')
        stub_configuration.then_write('Hello world!')

        actual_answer = stub_configuration.next_answer()

        self.assertEqual('Hello world!', actual_answer.stdout)
        self.assertEqual(None, actual_answer.stderr)
        self.assertEqual(0, actual_answer.return_code)


    def test_should_set_stderr_when_answering (self):
        stub_configuration = StubConfiguration('any_command', ['any_arg1', 'any_arg2'], 'any_stdin')
        stub_configuration.then_write(stderr='Hello error!')

        actual_answer = stub_configuration.next_answer()

        self.assertEqual(None, actual_answer.stdout)
        self.assertEqual('Hello error!', actual_answer.stderr)
        self.assertEqual(0, actual_answer.return_code)


    def test_should_set_stdout_and_stderr_with_chaining_when_answering (self):
        stub_configuration = StubConfiguration('any_command', ['any_arg1', 'any_arg2'], 'any_stdin')
        stub_configuration.then_write('Hello world!', 'Hello error!')

        actual_answer = stub_configuration.next_answer()

        self.assertEqual('Hello world!', actual_answer.stdout)
        self.assertEqual('Hello error!', actual_answer.stderr)
        self.assertEqual(0, actual_answer.return_code)


    def test_should_set_return_code_and_stderr_and_stdout (self):
        stub_configuration = StubConfiguration('any_command', ['any_arg1', 'any_arg2'], 'any_stdin')
        stub_configuration.then_answer('Hello world!', 'Hello error!', 15)

        actual_answer = stub_configuration.next_answer()

        self.assertEqual('Hello world!', actual_answer.stdout)
        self.assertEqual('Hello error!', actual_answer.stderr)
        self.assertEqual(15, actual_answer.return_code)


    def test_should_have_property_answers_with_empty_list (self):
        stub_configuration = StubConfiguration('any_command', ['any_arg1', 'any_arg2'], 'any_stdin')

        actual_answers = stub_configuration.answers
        
        self.assertEqual([], actual_answers)


    def test_should_raise_exception_when_asking_for_next_answer_when_no_answer_is_given (self):
        stub_configuration = StubConfiguration('any_command', ['any_arg1', 'any_arg2'], 'any_stdin')

        self.assertRaises(Exception, stub_configuration.next_answer)


    def test_should_set_arguments (self):
        stub_configuration = StubConfiguration('any_command')

        actual_return_value = stub_configuration.at_least_with_arguments('-arg1', '-arg2', '-arg3')

        self.assertEqual(stub_configuration, actual_return_value)
        self.assertEqual(['-arg1', '-arg2', '-arg3'], stub_configuration.command_input.arguments)


    def test_should_set_stdin (self):
        stub_configuration = StubConfiguration('any_command')

        actual_return_value = stub_configuration.with_input('stdin')

        self.assertEqual(stub_configuration, actual_return_value)
        self.assertEqual('stdin', stub_configuration.command_input.stdin)


    def test_should_allow_with_or_and_input (self):
        stub_configuration = StubConfiguration('any_command')

        self.assertEqual(stub_configuration.with_input, stub_configuration.and_input)


    def test_should_append_second_answer (self):
        stub_configuration = StubConfiguration('any_command', ['any_arg1', 'any_arg2'], 'any_stdin')
        stub_configuration.then_answer('Hello world!', 'Hello error!', 0)
        stub_configuration.then_answer('Foo bar!', 'Foo error!', 1)

        actual_count_of_answers = len(stub_configuration.answers)

        self.assertEqual(2, actual_count_of_answers)


    def test_should_send_two_different_answers_when_asking_for_next_answer_twice (self):
        stub_configuration = StubConfiguration('any_command', ['any_arg1', 'any_arg2'], 'any_stdin')
        stub_configuration.then_answer('Hello world!', 'Hello error!', 0)
        stub_configuration.then_answer('Foo bar!', 'Foo error!', 1)

        actual_first_answer = stub_configuration.next_answer()

        self.assertEqual('Hello world!', actual_first_answer.stdout)
        self.assertEqual('Hello error!', actual_first_answer.stderr)
        self.assertEqual(0, actual_first_answer.return_code)

        actual_second_answer = stub_configuration.next_answer()

        self.assertEqual('Foo bar!', actual_second_answer.stdout)
        self.assertEqual('Foo error!', actual_second_answer.stderr)
        self.assertEqual(1, actual_second_answer.return_code)


    def test_should_repeat_last_answer_when_asking_for_more_answers_than_given (self):
        stub_configuration = StubConfiguration('any_command', ['any_arg1', 'any_arg2'], 'any_stdin')
        stub_configuration.then_answer('Hello world!', 'Hello error!', 0)
        stub_configuration.then_answer('Foo bar!', 'Foo error!', 1)

        actual_first_answer = stub_configuration.next_answer()

        self.assertEqual('Hello world!', actual_first_answer.stdout)
        self.assertEqual('Hello error!', actual_first_answer.stderr)
        self.assertEqual(0, actual_first_answer.return_code)

        actual_second_answer = stub_configuration.next_answer()

        self.assertEqual('Foo bar!', actual_second_answer.stdout)
        self.assertEqual('Foo error!', actual_second_answer.stderr)
        self.assertEqual(1, actual_second_answer.return_code)

        actual_third_answer = stub_configuration.next_answer()

        self.assertEqual('Foo bar!', actual_third_answer.stdout)
        self.assertEqual('Foo error!', actual_third_answer.stderr)
        self.assertEqual(1, actual_third_answer.return_code)


    def test_should_send_answers_in_given_order_when_asking_for_next_answer (self):
        stub_configuration = StubConfiguration('any_command', ['any_arg1', 'any_arg2'], 'any_stdin')
        stub_configuration.then_answer('Hello world!', 'Hello error!', 0)
        stub_configuration.then_answer('Foo bar!', 'Foo error!', 1)
        stub_configuration.then_answer('Spam eggs!', 'Spam error!', 2)

        actual_first_answer = stub_configuration.next_answer()

        self.assertEqual('Hello world!', actual_first_answer.stdout)
        self.assertEqual('Hello error!', actual_first_answer.stderr)
        self.assertEqual(0, actual_first_answer.return_code)

        actual_second_answer = stub_configuration.next_answer()

        self.assertEqual('Foo bar!', actual_second_answer.stdout)
        self.assertEqual('Foo error!', actual_second_answer.stderr)
        self.assertEqual(1, actual_second_answer.return_code)

        actual_third_answer = stub_configuration.next_answer()

        self.assertEqual('Spam eggs!', actual_third_answer.stdout)
        self.assertEqual('Spam error!', actual_third_answer.stderr)
        self.assertEqual(2, actual_third_answer.return_code)


    def test_should_append_answer_when_using_method_then (self):
        stub_configuration = StubConfiguration('any_command', ['any_arg1', 'any_arg2'], 'any_stdin')

        stub_configuration.then(Answer('Hello world!', 'Hello error', 99))

        actual_count_of_answers = len(stub_configuration.answers)

        self.assertEqual(1, actual_count_of_answers)

        actual_answer = stub_configuration.next_answer()

        self.assertEqual('Hello world!', actual_answer.stdout)
        self.assertEqual('Hello error', actual_answer.stderr)
        self.assertEqual(99, actual_answer.return_code)


    def test_should_return_self_when_using_method_then (self):
        stub_configuration = StubConfiguration('any_command', ['any_arg1', 'any_arg2'], 'any_stdin')
        answer = Answer('Hello world!', 'Hello error', 99)

        actual_result = stub_configuration.then(answer)
        
        self.assertTrue(actual_result is not None, 'Not returning anything!')
        self.assertEqual(stub_configuration, actual_result)


    def test_should_return_self_when_using_method_then_answer (self):
        stub_configuration = StubConfiguration('any_command', ['any_arg1', 'any_arg2'], 'any_stdin')

        actual_result = stub_configuration.then_answer('Hello world!', 'Hello error', 99)

        self.assertTrue(actual_result is not None, 'Not returning anything!')
        self.assertEqual(stub_configuration, actual_result)


    def test_should_return_self_when_using_method_then_return (self):
        stub_configuration = StubConfiguration('any_command', ['any_arg1', 'any_arg2'], 'any_stdin')

        actual_result = stub_configuration.then_return(100)

        self.assertTrue(actual_result is not None, 'Not returning anything!')
        self.assertEqual(stub_configuration, actual_result)

    def test_should_return_self_when_using_method_then_write (self):
        stub_configuration = StubConfiguration('any_command', ['any_arg1', 'any_arg2'], 'any_stdin')

        actual_result = stub_configuration.then_write('Hello world.')

        self.assertTrue(actual_result is not None, 'Not returning anything!')
        self.assertEqual(stub_configuration, actual_result)


    def test_should_return_false_when_comparing_and_current_answer_is_different (self):
        stub_configuration1 = StubConfiguration('any_command', ['any_arg1', 'any_arg2'], 'any_stdin', [], 0)
        stub_configuration2 = StubConfiguration('any_command', ['any_arg1', 'any_arg2'], 'any_stdin', [], 1)

        self.assertFalse(stub_configuration1 == stub_configuration2, 'comparison error: attribute current_answer')


    def test_should_return_false_when_comparing_and_answers_are_different (self):
        stub_configuration1 = StubConfiguration('any_command', ['any_arg1', 'any_arg2'], 'any_stdin', [Answer('stdout1', 'stderr1', 0)], 0)
        stub_configuration2 = StubConfiguration('any_command', ['any_arg1', 'any_arg2'], 'any_stdin', [Answer('stdout2', 'stderr2', 1)], 0)

        self.assertFalse(stub_configuration1 == stub_configuration2, 'comparison error: attribute answers')


    def test_should_return_true_when_comparing_and_stub_configurations_are_equal (self):
        stub_configuration1 = StubConfiguration('any_command', ['any_arg1', 'any_arg2'], 'any_stdin', [Answer('stdout1', 'stderr1', 13)], 1)
        stub_configuration2 = StubConfiguration('any_command', ['any_arg1', 'any_arg2'], 'any_stdin', [Answer('stdout1', 'stderr1', 13)], 1)

        self.assertTrue(stub_configuration1 == stub_configuration2, 'comparison error: objects are equal')
        
    def test_should_return_string_with_all_properties (self):
        stub_configuration = StubConfiguration('any_command', ['any_arg1', 'any_arg2'], 'any_stdin', [Answer('stdout1', 'stderr1', 13)], 1)

        self.assertEqual("StubConfiguration {'current_answer': 1, 'answers': [{'return_code': 13, 'stderr': 'stderr1', 'stdout': 'stdout1'}], 'command_input': {'stdin': 'any_stdin', 'command': 'any_command', 'arguments': ['any_arg1', 'any_arg2']}}", str(stub_configuration))
