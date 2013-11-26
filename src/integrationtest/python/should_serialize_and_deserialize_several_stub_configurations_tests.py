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

from os.path import join

from shtub import deserialize_stub_configurations

import integrationtest_support


class Test (integrationtest_support.IntegrationTestSupport):

    def test(self):
        self.prepare_default_testbed(['command_stub1', 'command_stub2'])
        self.create_command_wrapper(
            'command_wrapper1', 'command_stub1', ['-arg1', '-arg2', '-arg3'], 'stdin1')
        self.create_command_wrapper(
            'command_wrapper2', 'command_stub2', ['-arg6', '-arg7', '-arg8'], 'stdin2')

        with self.fixture() as when:
            when.calling('command_stub1').at_least_with_arguments('-arg1', '-arg2', '-arg3').and_input('stdin1') \
                .then_answer('Hello world 1', 'Hello error 1', 0)
            when.calling('command_stub2').at_least_with_arguments('-arg6', '-arg7', '-arg8').and_input('stdin2') \
                .then_answer('Hello world 2', 'Hello error 2', 0)

        actual_return_code1 = self.execute_command('command_wrapper1')
        actual_return_code2 = self.execute_command('command_wrapper2')

        self.assertEqual(0, actual_return_code1)
        self.assertEqual(0, actual_return_code2)

        stub_configurations_filename = join(
            self.base_dir, 'shtub', 'stub-configurations')
        actual_stub_configurations = deserialize_stub_configurations(
            stub_configurations_filename)

        self.assertEqual(2, len(actual_stub_configurations))

        actual_first_stub_configuration = actual_stub_configurations[0]

        self.assertEqual(
            'stdin1', actual_first_stub_configuration.command_input.stdin)
        self.assertEqual(['-arg1', '-arg2', '-arg3'],
                         actual_first_stub_configuration.command_input.arguments)
        self.assertEqual(
            'command_stub1', actual_first_stub_configuration.command_input.command)

        actual_first_answer = actual_first_stub_configuration.next_answer()

        self.assertEqual('Hello world 1', actual_first_answer.stdout)
        self.assertEqual('Hello error 1', actual_first_answer.stderr)
        self.assertEqual(0, actual_first_answer.return_code)

        actual_second_stub_configuration = actual_stub_configurations[1]

        self.assertEqual(['-arg6', '-arg7', '-arg8'],
                         actual_second_stub_configuration.command_input.arguments)
        self.assertEqual(
            'stdin2', actual_second_stub_configuration.command_input.stdin)
        self.assertEqual(
            'command_stub2', actual_second_stub_configuration.command_input.command)

        actual_second_answer = actual_second_stub_configuration.next_answer()

        self.assertEqual('Hello world 2', actual_second_answer.stdout)
        self.assertEqual('Hello error 2', actual_second_answer.stderr)
        self.assertEqual(0, actual_second_answer.return_code)


if __name__ == '__main__':
    unittest.main()
