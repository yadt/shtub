import unittest

from os.path import join

from shtub import BASEDIR, deserialize_expectations

from integrationtest_support import IntegrationTestSupport


class Test (IntegrationTestSupport):
    def test (self):
        self.prepare_default_testbed(['command_stub'])
        
        self.create_command_wrapper('command_wrapper', 'command_stub', ['-arg1', '-arg2', '-arg3'], 'stdin')
        
        with self.fixture() as fixture:
            fixture.expect('command_stub', ['-arg1', '-arg2', '-arg3'], 'stdin') \
                   .then_answer('Hello world.', 'Hello error!', 2)

        expectations_filename = join(self.base_dir, BASEDIR, "expectations")
        actual_expectations = deserialize_expectations(expectations_filename)
        
        self.assertEquals(1, len(actual_expectations))
        
        actual_expectation = actual_expectations[0]
        
        self.assertEquals(['-arg1', '-arg2', '-arg3'], actual_expectation.arguments)
        self.assertEquals('stdin', actual_expectation.stdin)
        self.assertEquals('command_stub', actual_expectation.command)
        
        actual_answer = actual_expectation.next_answer()
        
        self.assertEquals('Hello world.', actual_answer.stdout)
        self.assertEquals('Hello error!', actual_answer.stderr)
        self.assertEquals(2, actual_answer.return_code)


if __name__ == '__main__':
    unittest.main()