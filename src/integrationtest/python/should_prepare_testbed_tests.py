import unittest

from os.path import exists, isdir, join, islink

import integrationtest_support


class Test (integrationtest_support.IntegrationTestSupport):
    def test (self):
        self.prepare_testbed({'env_var': 'env_value'}, ['command_stub1', 'command_stub2'])
        
        actual_testbase = self
        
        self.assertEquals({'env_var': 'env_value'}, actual_testbase.env)
        self.assertEquals(['command_stub1', 'command_stub2'], actual_testbase.stubs)
        
        self.assertTrue(isdir(actual_testbase.stubs_dir))
        
        for stub_name in ['command_stub1', 'command_stub2']:
            self.assertTrue(islink(join(actual_testbase.stubs_dir, stub_name)))

        test_execution_filename = join(actual_testbase.base_dir, 'test-execution')
        self.assertTrue(exists(test_execution_filename), 'directory test-execution does not exist')
        self.assertTrue(isdir(test_execution_filename), 'test-execution is not a directory!')


if __name__ == '__main__':
    unittest.main()
