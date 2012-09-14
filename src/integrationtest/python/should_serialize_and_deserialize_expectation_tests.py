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

from os.path import join

from shtub import deserialize_expectations

import integrationtest_support


class Test (integrationtest_support.IntegrationTestSupport):
    def test (self):
        # given
        self.prepare_default_testbed(['command_stub'])
        self.create_command_wrapper('command_wrapper', 'command_stub', ['-arg1', '-arg2', '-arg3'], 'stdin')

        # when
        with self.fixture() as when:
            when.calling('command_stub').with_arguments('-arg1', '-arg2', '-arg3').and_input('stdin') \
                .then_answer('Hello world.', 'Hello error!', 2)

        expectations_filename = join(self.base_dir, 'shtub', 'expectations')
        actual_expectations = deserialize_expectations(expectations_filename)

        # then
        self.assertEqual(1, len(actual_expectations))
        actual_expectation = actual_expectations[0]

        self.assertEqual(['-arg1', '-arg2', '-arg3'], actual_expectation.command_input.arguments)
        self.assertEqual('stdin', actual_expectation.command_input.stdin)
        self.assertEqual('command_stub', actual_expectation.command_input.command)

        actual_answer = actual_expectation.next_answer()

        self.assertEqual('Hello world.', actual_answer.stdout)
        self.assertEqual('Hello error!', actual_answer.stderr)
        self.assertEqual(2, actual_answer.return_code)


if __name__ == '__main__':
    unittest.main()
