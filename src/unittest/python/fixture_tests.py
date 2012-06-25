from mock import patch, call

from shtub.fixture import Fixture
from shtub.expectation import Expectation
from shtub.testbase import TestCase

class FixtureTest (TestCase):
    def test_should_create_object_with_given_base_dir_and_empty_list_of_expectations (self):
        actual_fixture = Fixture('/abc/def')
        
        self.assertEquals('/abc/def', actual_fixture.base_dir)
        self.assertEquals([], actual_fixture.expectations)
        
    def test_should_append_a_new_expectation (self):
        fixture = Fixture('/test123')
        
        fixture.expect('any_command', ['any_arg0', 'any_arg1', 'any_arg2'], 'any_stdin')
        
        actual_expectations = fixture.expectations
        self.assertEquals(1, len(actual_expectations))
        
        actual_expectation = actual_expectations[0]
        
        self.assertEquals('any_command', actual_expectation.command)
        self.assertEquals(['any_arg0', 'any_arg1', 'any_arg2'], actual_expectation.arguments)
        self.assertEquals('any_stdin', actual_expectation.stdin)

    def test_should_append_a_new_expectation_with_default_properties (self):
        fixture = Fixture('/test123')
        
        fixture.expect('any_command', ['any_arg0'], 'any_stdin')
        
        actual_expectations = fixture.expectations
        self.assertEquals(1, len(actual_expectations))
        
        actual_expectation = actual_expectations[0]
        
        self.assertEquals('any_command', actual_expectation.command)
        self.assertEquals(['any_arg0'], actual_expectation.arguments)
        self.assertEquals('any_stdin', actual_expectation.stdin)

    def test_should_append_two_new_expectations_in_correct_order (self):
        fixture = Fixture('/test123')
        
        fixture.expect('any_command1', ['1any_arg0', '1any_arg1', '1any_arg2'],'any_stdin')
        fixture.expect('any_command2', ['2any_arg0', '2any_arg1', '2any_arg2'], 'any_stdin2')
        
        actual_expectations = fixture.expectations
        self.assertEquals(2, len(actual_expectations))
        
        actual_first_expectation = actual_expectations[0]
        
        self.assertEquals('any_command1', actual_first_expectation.command)
        self.assertEquals(['1any_arg0', '1any_arg1', '1any_arg2'], actual_first_expectation.arguments)
        self.assertEquals('any_stdin', actual_first_expectation.stdin)
        
        actual_second_expectation = actual_expectations[1]
        
        self.assertEquals('any_command2', actual_second_expectation.command)
        self.assertEquals(['2any_arg0', '2any_arg1', '2any_arg2'], actual_second_expectation.arguments)
        self.assertEquals('any_stdin2', actual_second_expectation.stdin)
    
    @patch('shtub.fixture.serialize_stub_executions')
    def test_should_return_fixture_itself_when_entering_with_statement_and_serialize_expectations_when_exiting (self, serialize_mock):
        fixture = Fixture('/hello/world')
        
        with fixture as fix:
            self.assertEquals(fix, fixture)
        
        self.assertEquals(call('/hello/world/test-execution/expectations', []), serialize_mock.call_args)
            
    def test_should_return_expectation_object (self):
        fixture = Fixture('/test123')
        
        actual_result = fixture.expect('any_command', ['any_arg'], 'any_stdin')
        
        self.assertIsInstance(actual_result, Expectation)
        self.assertEquals('any_command', actual_result.command)
        self.assertEquals(['any_arg'], actual_result.arguments)
        self.assertEquals('any_stdin', actual_result.stdin)
        