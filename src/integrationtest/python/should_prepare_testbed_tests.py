import unittest
import os

import integrationtest_support


class Test (integrationtest_support.IntegrationTestSupport):

    def test (self):
        self.prepare_testbed({'env_var': 'env_value'}, ['command_stub1', 'command_stub2'])
        
        actual_testbase = self
        
        self.assertEquals({'env_var': 'env_value'}, actual_testbase.env)
        self.assertEquals(['command_stub1', 'command_stub2'], actual_testbase.stubs)
        
        self.assert_directory_exists(actual_testbase.stubs_dir)
        
        for stub_name in ['command_stub1', 'command_stub2']:
            symlink_to_stub = os.path.join(actual_testbase.stubs_dir, stub_name)
            self.assert_is_link(symlink_to_stub)

        test_execution_directory = os.path.join(actual_testbase.base_dir, 'test-execution')
        self.assert_directory_exists(test_execution_directory)


if __name__ == '__main__':
    unittest.main()
