import unittest
import os
import shutil
import subprocess
import tempfile

from shtub import BASEDIR, STUBS_DIR
from shtub.fixture import Fixture
from shtub.verifier import Verifier


class IntegrationTestBase (unittest.TestCase):
    def setUp (self):
        self.command_counter = 0
        self.set_base_dir(None)
        
    def tearDown (self):
        if self.cleanup_base_dir and os.path.exists(self.base_dir):
            shutil.rmtree(self.base_dir)
            
    def execute_command (self, command):
        shell_process = subprocess.Popen([command],
                                         stdout = subprocess.PIPE,
                                         stderr = subprocess.PIPE,
                                         shell  = True,
                                         cwd    = self.base_dir,
                                         env    = self.env)
        
        stdout, stderr = shell_process.communicate()
        
        normalized_command = command.replace(' ', '_')
        output_filename = os.path.join(self.base_dir,
                                       BASEDIR,
                                       '%02d-command-%s' % (self.command_counter, normalized_command))
        
        with open(output_filename, 'w') as outputfile:
            outputfile.write('----------------- ENVIRONMENT -------------------\n')
            
            for key in sorted(self.env.keys()):
                outputfile.write('%s=%s\n' % (key, self.env[key]))
                
            outputfile.write('----------------- STDOUT -------------------\n')
            outputfile.write(stdout)
            
            outputfile.write('----------------- STDERR -------------------\n')
            outputfile.write(stderr)

        self.command_counter += 1

        return shell_process.returncode

    def fixture (self):
        return Fixture(self.base_dir)
    
    def verify (self):
        return Verifier(self.base_dir)
    
    def prepare_testbed (self, env, stubs):
        self.env = env
        self.stubs = stubs
        
        os.mkdir(os.path.join(self.base_dir, BASEDIR))
        os.mkdir(self.stubs_dir)
        self.stub_commands(self.stubs)
    
    def stub_commands (self, command_list):
        command_stub_path = os.path.join(os.path.dirname(__file__), 'commandstub.py')
        
        for command in command_list:
            os.symlink(command_stub_path, os.path.join(self.stubs_dir, command))

    def make_base_dir (self, base_dir):
        os.makedirs(base_dir)
        self.set_base_dir(base_dir)

    def set_base_dir (self, base_dir):
        if base_dir:
            self.base_dir = base_dir
            self.cleanup_base_dir = False
        else:
            self.base_dir = tempfile.mkdtemp(prefix='integration-test-')
            self.cleanup_base_dir = True

        self.stubs_dir = os.path.join(self.base_dir, STUBS_DIR)


class TestCase (unittest.TestCase):
    def assertIsNone (self, given_object, msg=None):
        self.assertTrue(given_object is None, msg)
        
    def assertIsNotNone (self, given_object, msg=None):
        self.assertTrue(given_object is not None, msg)
        
    def assertIsInstance (self, given_object, class_or_type_or_tuple, msg=None):
        self.assertTrue(isinstance(given_object, class_or_type_or_tuple), msg)
