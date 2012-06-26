import unittest
import os
import shutil
import subprocess
import tempfile

from shtub import BASEDIR, STUBS_DIRECTORY
from shtub.fixture import Fixture
from shtub.verifier import Verifier


class IntegrationTestBase (unittest.TestCase):
    def setUp (self):
        self.command_counter = 0
        self.set_base_dir(None)
        
    def tearDown (self):
        if self.cleanup_base_dir and os.path.exists(self.base_dir):
            shutil.rmtree(self.base_dir)

    def _write_output_file (self, command, stdout, stderr):
        normalized_command = command.replace(' ', '_')
        filename = '%02d-command-%s' % (self.command_counter, normalized_command)
        output_path = os.path.join(self.base_dir, BASEDIR, filename)
        
        with open(output_path, 'w') as output_file:
            output_file.write('----------------- ENVIRONMENT -------------------\n')
            for key in sorted(self.env.keys()):
                output_file.write('%s=%s\n' % (key, self.env[key]))
            
            output_file.write('----------------- STDOUT -------------------\n')
            output_file.write(stdout)
            
            output_file.write('----------------- STDERR -------------------\n')
            output_file.write(stderr)

    def execute_command (self, command):
        shell_process = subprocess.Popen(args   = [command],
                                         stdout = subprocess.PIPE,
                                         stderr = subprocess.PIPE,
                                         shell  = True,
                                         cwd    = self.base_dir,
                                         env    = self.env)
        
        stdout, stderr = shell_process.communicate()
        self._write_output_file(command, stdout, stderr)
        self.command_counter += 1

        return shell_process.returncode

    def fixture (self):
        return Fixture(self.base_dir)
    
    def verify (self):
        return Verifier(self.base_dir)
    
    def prepare_testbed (self, env, stubs):
        self.env   = env
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
            self.base_dir         = base_dir
            self.cleanup_base_dir = False
        else:
            self.base_dir         = tempfile.mkdtemp(prefix='integration-test-')
            self.cleanup_base_dir = True

        self.stubs_dir = os.path.join(self.base_dir, STUBS_DIRECTORY)


class TestCase (unittest.TestCase):
    def assertIsNone (self, given_object, msg = None):
        self.assertTrue(given_object is None, msg)
        
    def assertIsNotNone (self, given_object, msg = None):
        self.assertTrue(given_object is not None, msg)
        
    def assertIsInstance (self, given_object, class_or_type_or_tuple, msg = None):
        self.assertTrue(isinstance(given_object, class_or_type_or_tuple), msg)
