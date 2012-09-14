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
import subprocess
import tempfile

from os import mkdir
from os.path import abspath, dirname, join


class Test (unittest.TestCase):
    def test (self):
        test_dir = tempfile.mkdtemp()
        self.write_expectations_json_file(test_dir, '[{\n'
                                                    '    "command_input": {\n'
                                                    '        "arguments": ["-arg1", "-arg2", "-arg3"],\n'
                                                    '        "command": "commandstub.py",\n'
                                                    '        "stdin": "Hello world."},\n'
                                                    '    "current_answer": 0,\n'
                                                    '    "answers": [\n'
                                                    '        {\n'
                                                    '            "stdout": "Hello world!",\n'
                                                    '            "stderr": "Hello error!",\n'
                                                    '            "return_code": 0\n'
                                                    '        }\n'
                                                    '    ]\n'
                                                    '}]')

        command_stub_path = abspath(join(dirname(__file__), '..', '..', 'main', 'python', 'shtub', 'commandstub.py'))

        shell_process = subprocess.Popen(args=[command_stub_path + ' -arg1 -arg2 -arg3'],
                                         stdin=subprocess.PIPE,
                                         stdout=subprocess.PIPE,
                                         stderr=subprocess.PIPE,
                                         shell=True,
                                         cwd=test_dir)

        stdout, stderr = shell_process.communicate(b'Hello world.')

        self.assertEqual(0, shell_process.returncode)

    def write_expectations_json_file(self, test_dir, expectation_json):
        test_execution_dir = join(test_dir, 'shtub')
        mkdir(test_execution_dir)

        expectations_filename = join(test_execution_dir, 'expectations')

        with open(expectations_filename, 'w') as expectations_file:
            expectations_file.write(expectation_json)

if __name__ == '__main__':
    unittest.main()
