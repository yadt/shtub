import unittest
import subprocess
import tempfile

from os import mkdir
from os.path import abspath, dirname, exists, join

from shtub.commandstub import handle_stub_call
from integrationtest_support import IntegrationTestSupport


class Test (IntegrationTestSupport):
    def test (self):
        test_dir              = tempfile.mkdtemp()
        test_execution_dir    = join(test_dir, 'test-execution')
        expectations_filename = join(test_execution_dir, 'expectations')
        
        mkdir(test_execution_dir)

        with open(expectations_filename, 'w') as expectations_file:
            expectation_json = """[{
    "arguments": ["-arg1", "-arg2", "-arg3"],
    "command": "not_commandstub.py",
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
            expectations_file.write(expectation_json)
            
        command_stub_path = abspath(join(dirname(__file__), '..', '..', 'main', 'python', 'shtub', 'commandstub.py'))

        shell_process = subprocess.Popen(args   = [command_stub_path + ' -arg1 -arg2 -arg3'],
                                         stdin  = subprocess.PIPE,
                                         stdout = subprocess.PIPE,
                                         stderr = subprocess.PIPE,
                                         shell  = True,
                                         cwd    = test_dir)

        stdout, stderr = shell_process.communicate('Hello world.')

        self.assertEquals(255, shell_process.returncode)


if __name__ == '__main__':
    unittest.main()