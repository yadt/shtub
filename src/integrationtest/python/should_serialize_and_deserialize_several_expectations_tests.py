import unittest

from os.path import join

from shtub import BASEDIR, deserialize_expectations

from shtub.frameworktestbase import FrameworkTestbase


class Test (FrameworkTestbase):
    def test (self):
        self.prepare_default_testbed(['command_stub1', 'command_stub2'])
        
        self.create_command_wrapper('command_wrapper1', 'command_stub1', ['-arg1', '-arg2', '-arg3'], 'stdin1')
        self.create_command_wrapper('command_wrapper2', 'command_stub2', ['-arg6', '-arg7', '-arg8'], 'stdin2')
        
        with self.fixture() as fixture:
            fixture.expect('command_stub1', ['-arg1', '-arg2', '-arg3'], 'stdin1') \
                   .then_answer('Hello world 1', 'Hello error 1', 0)
            fixture.expect('command_stub2', ['-arg6', '-arg7', '-arg8'], 'stdin2') \
                   .then_answer('Hello world 2', 'Hello error 2', 0)
        
        actual_return_code1 = self.execute_command('command_wrapper1')
        actual_return_code2 = self.execute_command('command_wrapper2')
        
        self.assertEquals(0, actual_return_code1)
        self.assertEquals(0, actual_return_code2)

        expectations_filename = join(self.base_dir, BASEDIR, "expectations")
        actual_expectations = deserialize_expectations(expectations_filename)
        
        self.assertEquals(2, len(actual_expectations))
        
        actual_first_expectation = actual_expectations[0]
        
        self.assertEquals('stdin1', actual_first_expectation.stdin)
        self.assertEquals(['-arg1', '-arg2', '-arg3'], actual_first_expectation.arguments)
        self.assertEquals('command_stub1', actual_first_expectation.command)
        
        actual_first_answer = actual_first_expectation.next_answer()
        
        self.assertEquals('Hello world 1', actual_first_answer.stdout)
        self.assertEquals('Hello error 1', actual_first_answer.stderr)
        self.assertEquals(0, actual_first_answer.return_code)
        
        actual_second_expectation = actual_expectations[1]

        self.assertEquals(['-arg6', '-arg7', '-arg8'], actual_second_expectation.arguments)
        self.assertEquals('stdin2', actual_second_expectation.stdin)
        self.assertEquals('command_stub2', actual_second_expectation.command)
        
        actual_second_answer = actual_second_expectation.next_answer()
        
        self.assertEquals('Hello world 2', actual_second_answer.stdout)
        self.assertEquals('Hello error 2', actual_second_answer.stderr)
        self.assertEquals(0, actual_second_answer.return_code)
        

if __name__ == '__main__':
    unittest.main()