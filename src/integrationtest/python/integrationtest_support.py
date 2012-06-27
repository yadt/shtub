import os

import shtub.testbase
from StringIO import StringIO


class IntegrationTestSupport (shtub.testbase.IntegrationTestBase):
    def create_command_wrapper (self, filename, command, arguments, stdin):
        wrapper_filename = os.path.join(self.stubs_dir, filename)
        joined_arguments = ' '.join(arguments)
        wrapper_content = """#!/usr/bin/env bash

echo -n %s | %s %s

""" % (stdin, command, joined_arguments)
        
        with open(wrapper_filename, 'w') as wrapper_file:
            wrapper_file.write(wrapper_content)
            
        os.chmod(wrapper_filename, 0o755)
        
    def create_path (self):
        path = self.stubs_dir
        
        if os.environ.has_key('PATH'):
            path += os.pathsep + os.environ['PATH']
        else:
            path += os.pathsep + '/bin'
            path += os.pathsep + '/usr/bin'
            path += os.pathsep + '/usr/local/bin'
        
        return path
    
    def create_python_path (self):
        pythonpath = os.path.abspath(os.path.join(os.path.abspath(__file__), '.'))
        pythonpath += os.pathsep 
        pythonpath += os.path.abspath(os.path.join(os.path.abspath(__file__), '..', '..', '..', 'main', 'python'))
        
        return pythonpath
    
    def prepare_default_testbed (self, stubs_list):
        path        = self.create_path()
        python_path = self.create_python_path()
        env         = {'PATH'       : path,
                       'PYTHONPATH' : python_path}
        
        self.prepare_testbed(env, stubs_list)

    def assert_file_content(self, command_wrapper_filename, expected_file_content):
        actual_file_content = StringIO()
        with open(command_wrapper_filename) as cmd_wrapper_file:
            for line in cmd_wrapper_file:
                actual_file_content.write(line)
        
        self.assertEquals(expected_file_content, actual_file_content.getvalue())

