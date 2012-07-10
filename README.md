shtub
=====

shell command stub

[![Build Status](https://secure.travis-ci.org/yadt/shtub.png?branch=master)](http://travis-ci.org/yadt/shtub)

Integration test framework which allows to *stub shell commands*:
if you have to assure that the application is calling the right shell commands in the correct order.

 A simple example stubbing the "ssh" command:
```python
class StubbingSshExampleTest (shtub.testbase.IntegrationTestBase):
    def test_should_stub_ssh_then_execute_ssh_and_verify_expectation (self):
        # given
        env = {'PATH': ..., 'PYTHONPATH': ...}
        stubs_list = ['ssh']
        self.prepare_testbed(env, stubs_list)

        with self.fixture() as fixture:
            fixture.expect('ssh', ['-arg1', '-arg2', '-arg3'], None).then_return(0)

        # when
        actual_return_code = self.execute_command('ssh -arg1 -arg2 -arg3')

        # then
        self.assertEquals(0, actual_return_code)

        with self.verify() as verifier:
            verifier.verify('ssh', ['-arg1', '-arg2', '-arg3'], None)

    # ...

# run the test
if __name__ == '__main__':
    unittest.main()
```
