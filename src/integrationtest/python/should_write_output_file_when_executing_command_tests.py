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

        actual_testbase = self

        self.assert_correct_output_file_content(actual_testbase, '00-command-command_wrapper')
        self.assert_correct_output_file_content(actual_testbase, '01-command-command_wrapper')


    def assert_correct_output_file_content(self, actual_testbase, output_filename):
        absolute_output_filename = join(actual_testbase.base_dir, BASEDIR, output_filename)
        self.assertTrue(exists(absolute_output_filename), 'Output file does not exist.')
        
        actual_file_content = StringIO()
        with open(absolute_output_filename) as cmd_wrapper_file:
            for line in cmd_wrapper_file:
                actual_file_content.write(line)
                
        expected_file_content = ("""----------------- ENVIRONMENT -------------------
PATH=%s
PYTHONPATH=%s
----------------- STDOUT -------------------
Hello world!
----------------- STDERR -------------------
Hello error.""") % (self.create_path(), self.create_python_path())
        
        self.assertEquals(expected_file_content, actual_file_content.getvalue())

    def assert_stub_links_created(self, actual_testbase, stubbed_local_command_list):
        self.assertTrue(isdir(actual_testbase.stubs_dir))
        
        for stub_name in stubbed_local_command_list:
            self.assertTrue(islink(join(actual_testbase.stubs_dir, stub_name)))


if __name__ == '__main__':
    unittest.main()
