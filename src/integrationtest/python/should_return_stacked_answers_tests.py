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

import integrationtest_support


class Tests (integrationtest_support.IntegrationTestSupport):
    def test (self):

        with self.fixture() as when:
            self.prepare_default_testbed(['command_stub'])
            when.calling('command_stub').at_least_with_arguments('arg')\
                .then_return(1).then_return(2).then_return(3)

        actual_return_code1 = self.execute_command('command_stub arg')
        actual_return_code2 = self.execute_command('command_stub arg')
        actual_return_code3 = self.execute_command('command_stub arg')

        self.assertEqual(1, actual_return_code1)
        self.assertEqual(2, actual_return_code2)
        self.assertEqual(3, actual_return_code3)

        with self.verify() as verify:
            verify.finished()


if __name__ == '__main__':
    unittest.main()
