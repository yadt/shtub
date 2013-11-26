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

import os
import sys
import stat

if sys.version_info[0] == 3:
    from io import StringIO
else:
    from StringIO import StringIO

import shtub.testbase


class IntegrationTestSupport (shtub.testbase.IntegrationTestBase):

    def create_command_wrapper(self, filename, command, arguments, stdin):
        wrapper_filename = os.path.join(self.stubs_dir, filename)
        joined_arguments = ' '.join(arguments)
        wrapper_content = ('#!/usr/bin/env bash\n'
                           '\n'
                           'echo -n %s | %s %s\n'
                           '\n'
                           ) % (stdin, command, joined_arguments)

        with open(wrapper_filename, 'wt') as wrapper_file:
            wrapper_file.write(wrapper_content)

        os.chmod(wrapper_filename, 0o755)

    def create_path(self):
        path = self.stubs_dir

        if 'PATH' in os.environ:
            path += os.pathsep + os.environ['PATH']
        else:
            path += os.pathsep + '/bin'
            path += os.pathsep + '/usr/bin'
            path += os.pathsep + '/usr/local/bin'

        return path

    def create_python_path(self):
        current_file = os.path.abspath(__file__)
        pythonpath = os.path.abspath(os.path.join(current_file, '.'))
        pythonpath += os.pathsep
        pythonpath += os.path.abspath(
            os.path.join(current_file, '..', '..', '..', 'main', 'python'))

        return pythonpath

    def create_environment(self):
        env = {'PATH': self.create_path(),
               'PYTHONPATH': self.create_python_path()}
        return env

    def prepare_default_testbed(self, stubs_list):
        env = self.create_environment()
        self.prepare_testbed(env, stubs_list)

    def assert_file_permissions(self, filename, expected_permissions):
        actual_permissions = stat.S_IMODE(os.stat(filename).st_mode)
        actual_permissions_as_oct = str(oct(actual_permissions))
        expected_permissions_as_oct = str(oct(expected_permissions))
        self.assertEqual(
            expected_permissions_as_oct, actual_permissions_as_oct)

    def assert_file_exists(self, filename):
        file_exists = os.path.exists(filename)
        self.assertTrue(file_exists, 'file %s does not exist!' % filename)

    def assert_file_content(self, filename, expected_file_content):
        actual_file_content_buffer = StringIO()

        with open(filename) as actual_file:
            for line in actual_file:
                actual_file_content_buffer.write(line)

        actual_file_content = actual_file_content_buffer.getvalue()
        self.assertEqual(expected_file_content, actual_file_content)

    def assert_directory_exists(self, directory_name):
        it_exists = os.path.exists(directory_name)
        self.assertTrue(
            it_exists, 'directory %s does not exist!' % directory_name)

        is_a_directory = os.path.isdir(directory_name)
        self.assertTrue(
            is_a_directory, '%s is not a directory!' % directory_name)

    def assert_is_link(self, filename):
        file_is_a_link = os.path.islink(filename)
        self.assertTrue(file_is_a_link, '%s is not a link!' % filename)
