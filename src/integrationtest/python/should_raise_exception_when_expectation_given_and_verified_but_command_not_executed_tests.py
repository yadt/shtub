import unittest

from os.path import join

import integrationtest_support


class Test (integrationtest_support.IntegrationTestSupport):       
    def test (self):
        self.prepare_default_testbed(['command_stub', 'command_stub1'])

        self.create_command_wrapper('command_wrapper1', 'command_stub1', ['-arg1', '-arg2', '-arg3'], 'stdin1')
        
        with self.fixture() as fixture:
            fixture.expect('command_stub', ['-arg0', '-arg2', '-arg3'], 'stdin') \
                   .then_answer('Hello world 1', 'Hello error 1', 0)
            fixture.expect('command_stub1', ['-arg1', '-arg2', '-arg3'], 'stdin1') \
                   .then_answer('Hello world 2', 'Hello error 2', 0)
            
        actual_return_code = self.execute_command('command_wrapper1')
        
        self.assertEquals(0, actual_return_code)
        
        with self.verify() as verifier:
            self.assertRaises(AssertionError, verifier.verify, 'command_stub', ['-arg1', '-arg2', '-arg3'], 'stdin')


if __name__ == '__main__':
    unittest.main()