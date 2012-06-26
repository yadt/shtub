import unittest

from os.path import join

from integrationtest_support import IntegrationTestSupport

from shtub import deserialize_stub_executions


class Test (IntegrationTestSupport):
    def test (self):
        self.prepare_default_testbed(['command_stub'])
                
        self.create_command_wrapper('command_wrapper', 'command_stub', ['-arg1', '-arg2', '-arg3'], 'stdin')
        
        with self.fixture() as fixture:
            fixture.expect('command_stub', ['-arg1', '-arg2', '-arg3'], 'stdin') \
                   .then_answer('Hello world.', 'Hello error!', 0)
        
        actual_return_code = self.execute_command('command_wrapper')
        
        self.assertEquals(0, actual_return_code)
        
        path = join(self.base_dir, 'test-execution', 'recorded-calls')
        
        actual_calls = deserialize_stub_executions(path)
        
        self.assertEquals(1, len(actual_calls))
        
        actual_call = actual_calls[0]
        
        self.assertEquals('command_stub', actual_call.command)
        self.assertEquals(['-arg1', '-arg2', '-arg3'], actual_call.arguments)
        self.assertEquals('stdin', actual_call.stdin)


if __name__ == '__main__':
    unittest.main()