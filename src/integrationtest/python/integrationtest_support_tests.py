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
import os

import integrationtest_support


class IntegrationTestSupportTest (integrationtest_support.IntegrationTestSupport):
    def test_should_create_command_wrapper (self):
        self.prepare_default_testbed(['command_stub'])
        self.create_command_wrapper('command_wrapper', 'command_stub', ['-arg1', '-arg2', '-arg3'], 'stdin')

        command_wrapper_filename = os.path.join(self.stubs_dir, 'command_wrapper')

        self.assert_file_exists(command_wrapper_filename)
        self.assert_file_permissions(command_wrapper_filename, 0o755)
        expected_wrapper_content = ('#!/usr/bin/env bash\n'
                                    '\n'
                                    'echo -n stdin | command_stub -arg1 -arg2 -arg3\n'
                                    '\n')
        self.assert_file_content(command_wrapper_filename, expected_wrapper_content)


if __name__ == '__main__':
    unittest.main()
