import unittest

import stat
import os

from os.path import exists, join
from StringIO import StringIO

import integrationtest_support


class IntegrationTestSupportTest (integrationtest_support.IntegrationTestSupport):
    def test_should_create_command_wrapper (self):
        self.prepare_default_testbed(['command_stub'])

        self.create_command_wrapper('command_wrapper', 'command_stub', ['-arg1', '-arg2', '-arg3'], 'stdin')
        
        command_wrapper_filename = join(self.stubs_dir, 'command_wrapper')
        
        self.assertTrue(exists(command_wrapper_filename))
        file_permissions = stat.S_IMODE(os.stat(command_wrapper_filename).st_mode)
        self.assertEqual(0o755, file_permissions)
        
        actual_file_content = StringIO()
        with open(command_wrapper_filename) as cmd_wrapper_file:
            for line in cmd_wrapper_file:
                actual_file_content.write(line)
            
        self.assertEquals('#!/usr/bin/env bash\n\necho -n stdin | command_stub -arg1 -arg2 -arg3\n\n', actual_file_content.getvalue())


if __name__ == '__main__':
    unittest.main()