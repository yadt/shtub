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

import sys

major, minor, micro, releaselevel, serial = sys.version_info
if major == 2 and minor == 6:
    import unittest2 as unittest
else:
    import unittest

from shtub.answer import Answer
from shtub.expectation import Expectation


class ExpectationTests (unittest.TestCase):
    def test_should_convert_dictionary_to_object (self):
        values = {'command'        : 'any_command',
                  'arguments'      : ['any_arg1', 'any_arg2', 'any_argument3'],
                  'stdin'          : 'any_stdin',
                  'current_answer' : 0,
                  'answers'        : [{'stdout'      : 'Hello world.',
                                       'stderr'      : 'Hello error!',
                                       'return_code' : 18},
                                      {'stdout'      : 'Spam eggs.',
                                       'stderr'      : 'Error!',
                                       'return_code' : 21}]
                  }

        actual_expectation = Expectation.from_dictionary(values)

        self.assertEquals('any_command', actual_expectation.command)
        self.assertEquals(['any_arg1', 'any_arg2', 'any_argument3'], actual_expectation.arguments)
        self.assertEquals('any_stdin', actual_expectation.stdin)
        self.assertEquals(0, actual_expectation.current_answer)

        actual_count_of_answers = len(actual_expectation.answers)

        self.assertEquals(2, actual_count_of_answers)

        actual_first_answer = actual_expectation.next_answer()

        self.assertEquals('Hello world.', actual_first_answer.stdout)
        self.assertEquals('Hello error!', actual_first_answer.stderr)
        self.assertEquals(18, actual_first_answer.return_code)

        actual_second_answer = actual_expectation.next_answer()

        self.assertEquals('Spam eggs.', actual_second_answer.stdout)
        self.assertEquals('Error!', actual_second_answer.stderr)
        self.assertEquals(21, actual_second_answer.return_code)


    def test_should_create_new_object_with_given_properties (self):
        expectation = Expectation('any_command', ['any_arg1', 'any_arg2'], 'any_stdin')

        self.assertEquals('any_command', expectation.command)
        self.assertEquals(['any_arg1', 'any_arg2'], expectation.arguments)
        self.assertEquals('any_stdin', expectation.stdin)
        self.assertEquals([], expectation.answers)
        self.assertEquals(0, expectation.current_answer)


    def test_should_create_new_object_with_given_properties_and_answers (self):
        answer1 = Answer('Abc', 'Def', 0)
        answer2 = Answer('Ghi', 'Jkl', 1)
        answer3 = Answer('Mno', 'Pqr', 2)
        answers = [answer1, answer2, answer3]

        expectation = Expectation('any_command', ['any_arg1', 'any_arg2'], 'any_stdin', answers, 2)

        self.assertEquals('any_command', expectation.command)
        self.assertEquals(['any_arg1', 'any_arg2'], expectation.arguments)
        self.assertEquals('any_stdin', expectation.stdin)
        self.assertEquals([answer1, answer2, answer3], expectation.answers)
        self.assertEquals(2, expectation.current_answer)


    def test_should_return_object_as_dictionary (self):
        expectation = Expectation('any_command', ['any_arg1', 'any_arg2'], 'any_stdin')
        expectation.then_answer('Hello world.', 'Hello error!', 19)

        actual_dictionary = expectation.as_dictionary()

        self.assertEquals('any_command', actual_dictionary['command'])
        self.assertEquals(['any_arg1', 'any_arg2'], actual_dictionary['arguments'])
        self.assertEquals('any_stdin', actual_dictionary['stdin'])
        self.assertEquals(0, actual_dictionary['current_answer'])
        actual_answer_dictionary = actual_dictionary['answers'][0]

        self.assertEquals('Hello world.', actual_answer_dictionary['stdout'])
        self.assertEquals('Hello error!', actual_answer_dictionary['stderr'])
        self.assertEquals(19, actual_answer_dictionary['return_code'])


    def test_should_set_return_code_when_answering (self):
        expectation = Expectation('any_command', ['any_arg1', 'any_arg2'], 'any_stdin')
        expectation.then_return(7)

        actual_answer = expectation.next_answer()

        self.assertEquals(None, actual_answer.stdout)
        self.assertEquals(None, actual_answer.stderr)
        self.assertEquals(7, actual_answer.return_code)


    def test_should_set_stdout_when_answering (self):
        expectation = Expectation('any_command', ['any_arg1', 'any_arg2'], 'any_stdin')
        expectation.then_write('Hello world!')

        actual_answer = expectation.next_answer()

        self.assertEquals('Hello world!', actual_answer.stdout)
        self.assertEquals(None, actual_answer.stderr)
        self.assertEquals(0, actual_answer.return_code)


    def test_should_set_stderr_when_answering (self):
        expectation = Expectation('any_command', ['any_arg1', 'any_arg2'], 'any_stdin')
        expectation.then_write(stderr='Hello error!')

        actual_answer = expectation.next_answer()

        self.assertEquals(None, actual_answer.stdout)
        self.assertEquals('Hello error!', actual_answer.stderr)
        self.assertEquals(0, actual_answer.return_code)


    def test_should_set_stdout_and_stderr_with_chaining_when_answering (self):
        expectation = Expectation('any_command', ['any_arg1', 'any_arg2'], 'any_stdin')
        expectation.then_write('Hello world!', 'Hello error!')

        actual_answer = expectation.next_answer()

        self.assertEquals('Hello world!', actual_answer.stdout)
        self.assertEquals('Hello error!', actual_answer.stderr)
        self.assertEquals(0, actual_answer.return_code)


    def test_should_set_return_code_and_stderr_and_stdout (self):
        expectation = Expectation('any_command', ['any_arg1', 'any_arg2'], 'any_stdin')
        expectation.then_answer('Hello world!', 'Hello error!', 15)

        actual_answer = expectation.next_answer()

        self.assertEquals('Hello world!', actual_answer.stdout)
        self.assertEquals('Hello error!', actual_answer.stderr)
        self.assertEquals(15, actual_answer.return_code)


    def test_should_have_property_answers_with_empty_list (self):
        expectation = Expectation('any_command', ['any_arg1', 'any_arg2'], 'any_stdin')

        self.assertEquals([], expectation.answers)


    def test_should_raise_exception_when_asking_for_next_answer_when_no_answer_is_given (self):
        expectation = Expectation('any_command', ['any_arg1', 'any_arg2'], 'any_stdin')

        self.assertRaises(Exception, expectation.next_answer)


    def test_should_set_arguments (self):
        expectation = Expectation('any_command')

        actual_return_value = expectation.with_arguments('-arg1', '-arg2', '-arg3')

        self.assertEquals(expectation, actual_return_value)
        self.assertEquals(['-arg1', '-arg2', '-arg3'], expectation.arguments)


    def test_should_set_stdin (self):
        expectation = Expectation('any_command')

        actual_return_value = expectation.with_input('stdin')

        self.assertEquals(expectation, actual_return_value)
        self.assertEquals('stdin', expectation.stdin)


    def test_should_allow_with_or_and_input (self):
        expectation = Expectation('any_command')

        self.assertEquals(expectation.with_input, expectation.and_input)


    def test_should_append_second_answer (self):
        expectation = Expectation('any_command', ['any_arg1', 'any_arg2'], 'any_stdin')
        expectation.then_answer('Hello world!', 'Hello error!', 0)
        expectation.then_answer('Foo bar!', 'Foo error!', 1)

        actual_count_of_answers = len(expectation.answers)

        self.assertEquals(2, actual_count_of_answers)


    def test_should_send_two_different_answers_when_asking_for_next_answer_twice (self):
        expectation = Expectation('any_command', ['any_arg1', 'any_arg2'], 'any_stdin')
        expectation.then_answer('Hello world!', 'Hello error!', 0)
        expectation.then_answer('Foo bar!', 'Foo error!', 1)

        actual_first_answer = expectation.next_answer()

        self.assertEquals('Hello world!', actual_first_answer.stdout)
        self.assertEquals('Hello error!', actual_first_answer.stderr)
        self.assertEquals(0, actual_first_answer.return_code)

        actual_second_answer = expectation.next_answer()

        self.assertEquals('Foo bar!', actual_second_answer.stdout)
        self.assertEquals('Foo error!', actual_second_answer.stderr)
        self.assertEquals(1, actual_second_answer.return_code)


    def test_should_repeat_last_answer_when_asking_for_more_answers_than_given (self):
        expectation = Expectation('any_command', ['any_arg1', 'any_arg2'], 'any_stdin')
        expectation.then_answer('Hello world!', 'Hello error!', 0)
        expectation.then_answer('Foo bar!', 'Foo error!', 1)

        actual_first_answer = expectation.next_answer()

        self.assertEquals('Hello world!', actual_first_answer.stdout)
        self.assertEquals('Hello error!', actual_first_answer.stderr)
        self.assertEquals(0, actual_first_answer.return_code)

        actual_second_answer = expectation.next_answer()

        self.assertEquals('Foo bar!', actual_second_answer.stdout)
        self.assertEquals('Foo error!', actual_second_answer.stderr)
        self.assertEquals(1, actual_second_answer.return_code)

        actual_third_answer = expectation.next_answer()

        self.assertEquals('Foo bar!', actual_third_answer.stdout)
        self.assertEquals('Foo error!', actual_third_answer.stderr)
        self.assertEquals(1, actual_third_answer.return_code)


    def test_should_send_answers_in_given_order_when_asking_for_next_answer (self):
        expectation = Expectation('any_command', ['any_arg1', 'any_arg2'], 'any_stdin')
        expectation.then_answer('Hello world!', 'Hello error!', 0)
        expectation.then_answer('Foo bar!', 'Foo error!', 1)
        expectation.then_answer('Spam eggs!', 'Spam error!', 2)

        actual_first_answer = expectation.next_answer()

        self.assertEquals('Hello world!', actual_first_answer.stdout)
        self.assertEquals('Hello error!', actual_first_answer.stderr)
        self.assertEquals(0, actual_first_answer.return_code)

        actual_second_answer = expectation.next_answer()

        self.assertEquals('Foo bar!', actual_second_answer.stdout)
        self.assertEquals('Foo error!', actual_second_answer.stderr)
        self.assertEquals(1, actual_second_answer.return_code)

        actual_third_answer = expectation.next_answer()

        self.assertEquals('Spam eggs!', actual_third_answer.stdout)
        self.assertEquals('Spam error!', actual_third_answer.stderr)
        self.assertEquals(2, actual_third_answer.return_code)


    def test_should_append_answer_when_using_method_then (self):
        expectation = Expectation('any_command', ['any_arg1', 'any_arg2'], 'any_stdin')

        expectation.then(Answer('Hello world!', 'Hello error', 99))

        actual_count_of_answers = len(expectation.answers)

        self.assertEquals(1, actual_count_of_answers)

        actual_answer = expectation.next_answer()

        self.assertEquals('Hello world!', actual_answer.stdout)
        self.assertEquals('Hello error', actual_answer.stderr)
        self.assertEquals(99, actual_answer.return_code)


    def test_should_return_self_when_using_method_then (self):
        expectation = Expectation('any_command', ['any_arg1', 'any_arg2'], 'any_stdin')
        answer = Answer('Hello world!', 'Hello error', 99)

        actual_result = expectation.then(answer)
        self.assertIsNotNone(actual_result, 'Not returning anything!')
        self.assertEquals(expectation, actual_result)


    def test_should_return_self_when_using_method_then_answer (self):
        expectation = Expectation('any_command', ['any_arg1', 'any_arg2'], 'any_stdin')

        actual_result = expectation.then_answer('Hello world!', 'Hello error', 99)

        self.assertIsNotNone(actual_result, 'Not returning anything!')
        self.assertEquals(expectation, actual_result)


    def test_should_return_self_when_using_method_then_return (self):
        expectation = Expectation('any_command', ['any_arg1', 'any_arg2'], 'any_stdin')

        actual_result = expectation.then_return(100)

        self.assertIsNotNone(actual_result, 'Not returning anything!')
        self.assertEquals(expectation, actual_result)

    def test_should_return_self_when_using_method_then_write (self):
        expectation = Expectation('any_command', ['any_arg1', 'any_arg2'], 'any_stdin')

        actual_result = expectation.then_write('Hello world.')

        self.assertIsNotNone(actual_result, 'Not returning anything!')
        self.assertEquals(expectation, actual_result)


    def test_should_return_false_when_comparing_and_current_answer_is_different (self):
        expectation1 = Expectation('any_command', ['any_arg1', 'any_arg2'], 'any_stdin', [], 0)
        expectation2 = Expectation('any_command', ['any_arg1', 'any_arg2'], 'any_stdin', [], 1)

        self.assertFalse(expectation1 == expectation2, 'comparison error: attribute current_answer')


    def test_should_return_false_when_comparing_and_answers_are_different (self):
        expectation1 = Expectation('any_command', ['any_arg1', 'any_arg2'], 'any_stdin', [Answer('stdout1', 'stderr1', 0)], 0)
        expectation2 = Expectation('any_command', ['any_arg1', 'any_arg2'], 'any_stdin', [Answer('stdout2', 'stderr2', 1)], 0)

        self.assertFalse(expectation1 == expectation2, 'comparison error: attribute answers')


    def test_should_return_true_when_comparing_and_expectations_are_equal (self):
        expectation1 = Expectation('any_command', ['any_arg1', 'any_arg2'], 'any_stdin', [Answer('stdout1', 'stderr1', 13)], 1)
        expectation2 = Expectation('any_command', ['any_arg1', 'any_arg2'], 'any_stdin', [Answer('stdout1', 'stderr1', 13)], 1)

        self.assertTrue(expectation1 == expectation2, 'comparison error: objects are equal')
