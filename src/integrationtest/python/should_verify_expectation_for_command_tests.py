import unittest

import integrationtest_support


class Tests (integrationtest_support.IntegrationTestSupport):
    def test (self):
        self.prepare_default_testbed(['command_stub'])
        self.create_command_wrapper('command_wrapper', 'command_stub', ['-arg1', '-arg2', '-arg3'], 'stdin' )

        with self.fixture() as fixture:
            fixture.expect('command_stub', ['-arg1', '-arg2', '-arg3'], 'stdin') \
                   .then_answer('Hello world!', 'Hello error!', 0) \
                   .then_return(1)

        actual_return_code1 = self.execute_command('command_wrapper')
        actual_return_code2 = self.execute_command('command_wrapper')

        self.assertEquals(0, actual_return_code1)
        self.assertEquals(0, actual_return_code2)

        with self.verify() as verifier:
            verifier.verify('command_stub', ['-arg1', '-arg2', '-arg3'], 'stdin')
            verifier.verify('command_stub', ['-arg1', '-arg2', '-arg3'], 'stdin')


if __name__ == '__main__':
    unittest.main()