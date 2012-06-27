import unittest

from os.path import exists, isdir, islink, join

from StringIO import StringIO

from shtub import BASEDIR
import integrationtest_support


class Test (integrationtest_support.IntegrationTestSupport):
    def test (self):
        self.prepare_default_testbed(['command_stub'])
        self.create_command_wrapper('command_wrapper', 'command_stub', ['-arg1', '-arg2', '-arg3'], 'stdin')

        with self.fixture() as fixture:
            fixture.expect('command_stub', ['-arg1', '-arg2', '-arg3'], 'stdin') \
                   .then_answer('Hello world!\n', 'Hello error.', 0)

        self.execute_command('command_wrapper')
        self.execute_command('command_wrapper')

        expected_file_content = ("""----------------- ENVIRONMENT -------------------
PATH=%s
PYTHONPATH=%s
----------------- STDOUT -------------------
Hello world!
----------------- STDERR -------------------
Hello error.""") % (self.create_path(), self.create_python_path())

        output_filename_00 = join(self.base_dir, 'test-execution', '00-command-command_wrapper')
        self.assert_file_content(output_filename_00, expected_file_content)
        
        output_filename_01 = join(self.base_dir, 'test-execution', '01-command-command_wrapper')
        self.assert_file_content(output_filename_01, expected_file_content)


if __name__ == '__main__':
    unittest.main()
