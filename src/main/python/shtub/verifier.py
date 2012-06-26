from os.path import join
from shtub import BASEDIR, deserialize_stub_executions
from shtub.execution import Execution


class Verifier (object):
    def __init__ (self, basedir):
        self.base_dir = basedir

    def verify (self, command, arguments, stdin):
        expectation = Execution(command, arguments, stdin)

        if not self.recorded_calls:
            raise AssertionError('No more recorded calls when verifying %s' % expectation)
        
        if not self.recorded_calls[0].fulfills(expectation):
            raise AssertionError('Recorded call (execution) does not fulfill expectation:\n'
                               + 'Expected %s\nActual   %s\n' % (expectation, self.recorded_calls[0]))
        
        self.recorded_calls = self.recorded_calls[1:]
    
    def __enter__ (self):
        filename = join(self.base_dir, BASEDIR, 'recorded-calls')
        self.recorded_calls = deserialize_stub_executions(filename)
        return self
    
    def __exit__(self, exception_type, exception_value, traceback):
        pass
