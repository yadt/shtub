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
import shtub.testbase

class StubbingSshExampleTest (shtub.testbase.IntegrationTestBase):
    def test_should_stub_ssh_then_execute_ssh_and_verify_expectation (self):
        env = self._create_environment()
        self.prepare_testbed(env, ['ssh'])

        with self.fixture() as when:
            when.calling('ssh').at_least_with_arguments('-arg1', '-arg2', '-arg3') \
                .then_return(0)

        actual_return_code = self.execute_command('ssh -arg1 -arg2 -arg3')

        self.assertEqual(0, actual_return_code)

        with self.verify() as verify:
            verify.called('ssh').with_arguments('-arg1', '-arg2', '-arg3')


    def _create_environment(self):
        env = {'PATH'       : self._create_path(),
               'PYTHONPATH' : self._create_python_path()}
        return env


    def _create_path (self):
        path = self.stubs_dir

        if 'PATH' in os.environ:
            path += os.pathsep + os.environ['PATH']
        else:
            path += os.pathsep + '/bin'
            path += os.pathsep + '/usr/bin'
            path += os.pathsep + '/usr/local/bin'

        return path


    def _create_python_path (self):
        current_file = os.path.abspath(__file__)
        pythonpath = os.path.abspath(os.path.join(current_file, '.'))
        pythonpath += os.pathsep
        pythonpath += os.path.abspath(os.path.join(current_file, '..', '..', '..', 'main', 'python'))

        return pythonpath


if __name__ == '__main__':
    unittest.main()
