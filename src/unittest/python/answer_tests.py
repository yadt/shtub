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

from shtub.answer import Answer


class AnswerTest (unittest.TestCase):
    def test_should_create_new_instance_with_given_values (self):
        actual = Answer('Hello world!', 'Hello error!', 8)

        self.assertEqual('Hello world!', actual.stdout)
        self.assertEqual('Hello error!', actual.stderr)
        self.assertEqual(8, actual.return_code)


    def test_should_return_answer_from_dictionary (self):
        answer_dictionary = {'stdout'      : 'Hello world.',
                             'stderr'      : 'Hello error!',
                             'return_code' : 82}

        actual_answer = Answer.from_dictionary(answer_dictionary)

        self.assertEqual('Hello world.', actual_answer.stdout)
        self.assertEqual('Hello error!', actual_answer.stderr)
        self.assertEqual(82, actual_answer.return_code)


    def test_should_return_answer_as_dictionary (self):
        answer = Answer('Hello world.', 'Hello error!', 13)

        actual_dictionary = answer.as_dictionary()

        self.assertEqual('Hello world.', actual_dictionary['stdout'])
        self.assertEqual('Hello error!', actual_dictionary['stderr'])
        self.assertEqual(13, actual_dictionary['return_code'])


    def test_should_return_answer_as_string (self):
        answer = Answer('Hello world.', 'Hello error!', 13)

        actual_string = answer.__str__()

        self.assertEqual("Answer {'return_code': 13, 'stderr': 'Hello error!', 'stdout': 'Hello world.'}", actual_string)


    def test_should_return_false_when_comparing_and_stdout_is_different (self):
        answer1 = Answer('Hello world.', 'Hello error!', 13)
        answer2 = Answer('Spam eggs', 'Hello error!', 13)

        self.assertFalse(answer1 == answer2, 'comparison error: attribute stdout')


    def test_should_return_false_when_comparing_and_stdout_is_different (self):
        answer1 = Answer('Hello world.', 'Hello error!', 13)
        answer2 = Answer('Hello world.', 'Spam eggs', 13)

        self.assertFalse(answer1 == answer2, 'comparison error: attribute stderr')


    def test_should_return_false_when_comparing_and_return_code_is_different (self):
        answer1 = Answer('Hello world.', 'Hello error!', 13)
        answer2 = Answer('Hello world.', 'Hello error!', 0)

        self.assertFalse(answer1 == answer2, 'comparison error: attribute return_code')


    def test_should_return_true_when_comparing_and_objects_are_equal (self):
        answer1 = Answer('Hello world.', 'Hello error!', 0)
        answer2 = Answer('Hello world.', 'Hello error!', 0)

        self.assertTrue(answer1 == answer2, 'comparison error: objects are equal')
