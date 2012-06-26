import os

from shtub import BASEDIR, serialize_stub_executions
from shtub.expectation import Expectation

class Fixture (object):
    def __init__ (self, basedir):
        self.base_dir     = basedir
        self.expectations = []
        
    def expect (self, command, arguments, stdin):
        expectation = Expectation(command, arguments, stdin)
        self.expectations.append(expectation)
        
        return expectation
    
    def __enter__ (self):
        return self
    
    def __exit__(self, exception_type, exception_value, traceback):
        __pychecker__ = 'unusednames=exception_type,exception_value,traceback'
        filename = os.path.join(self.base_dir, BASEDIR, 'expectations')
        
        serialize_stub_executions(filename, self.expectations)
