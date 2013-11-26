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

import integrationtest_support

from shtub import deserialize_executions


class Test (integrationtest_support.IntegrationTestSupport):

    def test(self):
        self.prepare_default_testbed(['command_stub'])
        self.create_command_wrapper(
            'command_wrapper', 'command_stub', ['-arg1', '-arg2', '-arg3'], 'stdin')

        with self.fixture() as when:
            when.calling('command_stub').at_least_with_arguments('-arg1', '-arg2', '-arg3').and_input('stdin') \
                .then_answer('Hello world.', 'Hello error!', 0)

        actual_return_code = self.execute_command('command_wrapper')

        self.assertEqual(0, actual_return_code)

        path = join(self.base_dir, 'shtub', 'executions')

        actual_executions = deserialize_executions(path)

        self.assertEqual(1, len(actual_executions))

        actual_execution = actual_executions[0]

        self.assertEqual(
            'command_stub', actual_execution.command_input.command)
        self.assertEqual(
            ['-arg1', '-arg2', '-arg3'], actual_execution.command_input.arguments)
        self.assertEqual('stdin', actual_execution.command_input.stdin)


if __name__ == '__main__':
    unittest.main()
