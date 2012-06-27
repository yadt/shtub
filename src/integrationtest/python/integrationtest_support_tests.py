import unittest

import stat
import os

from os.path import exists, join

import integrationtest_support


class IntegrationTestSupportTest (integrationtest_support.IntegrationTestSupport):
    def test_should_create_command_wrapper (self):
        self.prepare_default_testbed(['command_stub'])

        self.create_command_wrapper('command_wrapper', 'command_stub', ['-arg1', '-arg2', '-arg3'], 'stdin')
        
        command_wrapper_filename = join(self.stubs_dir, 'command_wrapper')
        
        self.assertTrue(exists(command_wrapper_filename))
        file_permissions = stat.S_IMODE(os.stat(command_wrapper_filename).st_mode)
        self.assertEqual(0o755, file_permissions)
        
        expected_file_content = """#!/usr/bin/env bash

echo -n stdin | command_stub -arg1 -arg2 -arg3

"""
        self.assert_file_content(command_wrapper_filename, expected_file_content)


if __name__ == '__main__':
    unittest.main()