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
import unittest

from os.path import join

if sys.version_info[0] == 3:
    from io import StringIO
else:
    from StringIO import StringIO

from shtub import BASEDIR
import integrationtest_support


class Test (integrationtest_support.IntegrationTestSupport):
    def test (self):
        self.prepare_default_testbed(['command_stub'])
        self.create_command_wrapper('command_wrapper', 'command_stub', ['-arg1', '-arg2', '-arg3'], 'stdin')

        with self.fixture() as when:
            when.calling('command_stub').with_arguments('-arg1', '-arg2', '-arg3').and_input('stdin') \
                .then_answer('Hello world!\n', 'Hello error.', 0)

        self.execute_command('command_wrapper')
        self.execute_command('command_wrapper')

        expected_file_content = ('--------------- ENVIRONMENT ----------------\n'
                                 'PATH=%s\n'
                                 'PYTHONPATH=%s\n'
                                 '----------------- STDOUT -------------------\n'
                                 'Hello world!\n'
                                 '----------------- STDERR -------------------\n'
                                 'Hello error.'
                                ) % (self.create_path(), self.create_python_path())

        output_filename_00 = join(self.base_dir, 'test-execution', '00-command_wrapper')
        self.assert_file_content(output_filename_00, expected_file_content)

        output_filename_01 = join(self.base_dir, 'test-execution', '01-command_wrapper')
        self.assert_file_content(output_filename_01, expected_file_content)


if __name__ == '__main__':
    unittest.main()
