#   shtub - shell command stub
#   Copyright (C) 2012 Immobilien Scout GmbH
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

__author__ = 'Alexander Metzner, Michael Gruber, Udo Juettner'

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


    def _normalize_command_line(self, command):
        normalized = command.replace(' ', '_') \
                            .replace('*', '_') \
                            .replace('?', '_') \
                            .replace(':', '_') \
                            .replace('/', '_')
        return normalized


    def _write_output_file (self, command, stdout, stderr):
        normalized = self._normalize_command_line(command)
        filename = '%02d-%s' % (self.command_counter, normalized)
        output_path = os.path.join(self.base_dir, BASEDIR, filename)

        with open(output_path, 'wb') as output_file:
            output_file.write('--------------- ENVIRONMENT ----------------\n')
            for key in sorted(self.env.keys()):
                output_file.write('%s=%s\n' % (key, self.env[key]))

            output_file.write('----------------- STDOUT -------------------\n')
            output_file.write(stdout)

            output_file.write('----------------- STDERR -------------------\n')
            output_file.write(stderr)


    def execute_command (self, command):
        shell_process = subprocess.Popen(args=[command],
                                         stdout=subprocess.PIPE,
                                         stderr=subprocess.PIPE,
                                         shell=True,
                                         cwd=self.base_dir,
                                         env=self.env)

        stdout, stderr = shell_process.communicate()
        self._write_output_file(command, stdout, stderr)
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
        current_path = os.path.dirname(__file__)
        command_stub_path = os.path.join(current_path, 'commandstub.py')

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

        self.stubs_dir = os.path.join(self.base_dir, STUBS_DIRECTORY)
