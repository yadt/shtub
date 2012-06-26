import unittest
import subprocess
import tempfile

from os import mkdir
from os.path import abspath, dirname, join


class Test (unittest.TestCase):
    def test (self):
        test_dir              = tempfile.mkdtemp()
        test_execution_dir    = join(test_dir, 'test-execution')
        expectations_filename = join(test_execution_dir, 'expectations')
        command_stub_path     = abspath(join(dirname(__file__), '..', '..', 'main', 'python', 'shtub', 'commandstub.py'))
        expectation_json      = """[{
    "arguments": ["-arg1", "-arg2", "-arg3"],
    "command": "commandstub.py",
    "stdin": "Hello world.",
    "current_answer": 0,
    "answers": [
        {
            "stdout": "Hello world!",
            "stderr": "Hello error!",
            "return_code": 0
        }
    ]
}]"""

        mkdir(test_execution_dir)

        with open(expectations_filename, 'w') as expectations_file:
            expectations_file.write(expectation_json)

        shell_process = subprocess.Popen(args   = [command_stub_path + ' -arg1 -arg2 -arg3'],
                                         stdin  = subprocess.PIPE,
                                         stdout = subprocess.PIPE,
                                         stderr = subprocess.PIPE,
                                         shell  = True,
                                         cwd    = test_dir)

        stdout, stderr = shell_process.communicate('Hello world.')

        print stdout, stderr
        self.assertEquals(0, shell_process.returncode)


if __name__ == '__main__':
    unittest.main()