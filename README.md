shtub [![Build Status](https://secure.travis-ci.org/yadt/shtub.png?branch=master)](http://travis-ci.org/yadt/shtub)
=====

shell command stub

Integration test framework which *stubs shell commands*.
The *stubs* can be *configured* and send back corresponding *answers*.
The executions of *stubs* can be *verified* (correct arguments and call order).

# Usage

## A simple example stubbing the "ssh" command:
```python
class StubbingSshExampleTest (shtub.testbase.IntegrationTestBase):
    def test_should_stub_ssh_then_execute_ssh_and_verify(self):
        # given
        env = {'PATH': ..., 'PYTHONPATH': ...}
        stubs_list = ['ssh']
        self.prepare_testbed(env, stubs_list)

        with self.fixture() as when:
            when.calling('ssh').at_least_with_arguments('-arg1', '-arg2', '-arg3').then_return(0)

        # when
        actual_return_code = self.execute_command('ssh -arg1 -arg2 -arg3')

        # then
        self.assertEquals(0, actual_return_code)

        with self.verify() as verify:
            verify.called('ssh').at_least_with_arguments('-arg1', '-arg2', '-arg3')
```
## Matching
You can match stub executions using invocation chaining with
  * with_input
  * at_least_with_arguments  

### Example
```python
when.calling('cmd').at_least_with_arguments('foo', '--verbose=1').with_input('Lorem ipsum dolorem').then_return(0)
```

## Answers
Answers describe what happens when a stubbed command is invoked.
Available answers :
  * `then_answer(stdout=None, stderr=None, return_code=0, milliseconds_to_wait=None)`
  * `then_return(return_code, milliseconds_to_wait=None)`
  * `then_write(stdout=None, stderr=None, milliseconds_to_wait=None)`

## Filtering verifications
The verify() methods need to verify executions in the same order in which they happened.
This means if your program calls 'ssh foo --bar' and then 'ssh bar --foo' then you will need to verify in the same order.
If you cannot determine the order (for example if your program is parallelized), you can filter the verifications like so :
```python
with self.verify() as complete_verify:
    with complete_verify.filter_by_argument('bar') as verify:
         verify.called('ssh').at_least_with_arguments('bar', '--foo')
    with complete_verify.filter_by_argument('foo') as verify:
         verify.called('ssh').at_least_with_arguments('foo', '--bar')
    complete_verify.finished()
```
## Using stacked answers
If your stubbed command should behave differently when called repeatedly, you can use stacked answers like so:

```python
when.calling('ssh').at_least_with_arguments('-arg1').then_return(0).then_return(100)
```
This will cause the first ssh call to succeed with exit code 0 and the next call to fail with exit code 100.



# Running a shtub test
if __name__ == '__main__':
    unittest.main()
```

If you are using *shtub* within a continuous integration system like buildbot,
make sure you are starting the process in a terminal (for buildbot: usePTY=True).

License
=======

shtub - shell command stub
Copyright (C) 2012-2013 Immobilien Scout GmbH

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

