import unittest
import os
import shtub.testbase

class StubbingSshExampleTest (shtub.testbase.IntegrationTestBase):
    def test_should_stub_ssh_then_execute_ssh_and_verify_expectation (self):
        env = {'PATH'       : self._path(),
               'PYTHONPATH' : self._python_path()}
        
        self.prepare_testbed(env, ['ssh'])

        with self.fixture() as fixture:
            fixture.expect('ssh', ['-arg1', '-arg2', '-arg3'], None) \
                   .then_return(0)

        actual_return_code = self.execute_command('ssh -arg1 -arg2 -arg3')

        self.assertEquals(0, actual_return_code)

        with self.verify() as verifier:
            verifier.verify('ssh', ['-arg1', '-arg2', '-arg3'], None)

    def _path (self):
        path = self.stubs_dir
        
        if os.environ.has_key('PATH'):
            path += os.pathsep + os.environ['PATH']
        else:
            path += os.pathsep + '/bin'
            path += os.pathsep + '/usr/bin'
            path += os.pathsep + '/usr/local/bin'
        
        return path
    
    def _python_path (self):
        current_file = os.path.abspath(__file__)
        pythonpath = os.path.abspath(os.path.join(current_file, '.'))
        pythonpath += os.pathsep 
        pythonpath += os.path.abspath(os.path.join(current_file, '..', '..', '..', 'main', 'python'))
        
        return pythonpath
    

if __name__ == '__main__':
    unittest.main()
