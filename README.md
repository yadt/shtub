shtub [![Build Status](https://secure.travis-ci.org/yadt/shtub.png?branch=master)](http://travis-ci.org/yadt/shtub)
=====

shell command stub

Integration test framework which *stubs shell commands*.
The stubs can be configured with *expectations* and send back corresponding
*answers* if expectations are fulfilled. The expectations can be *verified*
(correct arguments and order).


 A simple example stubbing the "ssh" command:
```python
class StubbingSshExampleTest (shtub.testbase.IntegrationTestBase):
    def test_should_stub_ssh_then_execute_ssh_and_verify_expectation (self):
        # given
        env = {'PATH': ..., 'PYTHONPATH': ...}
        stubs_list = ['ssh']
        self.prepare_testbed(env, stubs_list)

        with self.fixture() as when:
            when.calling('ssh').with_arguments('-arg1', '-arg2', '-arg3').then_return(0)

        # when
        actual_return_code = self.execute_command('ssh -arg1 -arg2 -arg3')

        # then
        self.assertEquals(0, actual_return_code)

        with self.verify() as verify:
            verify.called('ssh').with_arguments('-arg1', '-arg2', '-arg3')

    # ...

# run the test
if __name__ == '__main__':
    unittest.main()
```

License
=======

shtub - shell command stub
Copyright (C) 2012 Immobilien Scout GmbH

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

