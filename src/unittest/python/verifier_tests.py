import unittest

from mock import patch, call

from shtub.verifier import Verifier
from shtub.execution import Execution

class VerfierTest (unittest.TestCase):
    def test_should_create_object_with_given_base_dir (self):
        actual_verifier = Verifier('/abc/def')
        
        self.assertEquals('/abc/def', actual_verifier.base_dir)
    
    @patch('shtub.verifier.deserialize_stub_executions')
    def test_should_deserialize_recorded_calls_and_return_verifier_itself_when_entering_with_statement (self, deserialize_mock):
        verifier = Verifier('/hello/world')
                
        with verifier as veri:
            self.assertEquals(veri, verifier)
            
        self.assertEquals(call('/hello/world/test-execution/recorded-calls'), deserialize_mock.call_args)
    
    @patch('shtub.verifier.deserialize_stub_executions')
    def test_should_raise_exception_when_no_executed_calls_recorded (self, deserialize_mock):
        verifier = Verifier('/hello/world')
        
        deserialize_mock.return_value = None
        
        with verifier as veri:
            self.assertRaises(AssertionError, veri.verify, 'any_stub', ['any_arguments'], 'any_stdin')

        self.assertEquals(call('/hello/world/test-execution/recorded-calls'), deserialize_mock.call_args)

    @patch('shtub.verifier.deserialize_stub_executions')
    def test_should_raise_exception_when_recorded_call_does_not_fit_expectation (self, deserialize_mock):
        verifier = Verifier('/hello/world')
        
        stub_execution = Execution('any_command', ['any_arg1', 'any_arg2'], 'any_stdin')
        
        deserialize_mock.return_value = [stub_execution]
        
        with verifier as veri:
            self.assertRaises(AssertionError, veri.verify, 'other_command', ['any_arg1', 'any_arg2'], 'any_stdin')

        self.assertEquals(call('/hello/world/test-execution/recorded-calls'), deserialize_mock.call_args)

    @patch('shtub.verifier.deserialize_stub_executions')
    def test_should_raise_exception_when_second_recorded_call_does_not_fit_expectation (self, deserialize_mock):
        verifier = Verifier('/hello/world')
        
        stub_execution1 = Execution('any_command1', ['1any_arg1', '1any_arg2'], 'any_stdin')
        stub_execution2 = Execution('any_command2', ['2any_arg1', '2any_arg2'], 'any_stdin2')
        
        deserialize_mock.return_value = [stub_execution1, stub_execution2]
        
        with verifier as veri:
            veri.verify('any_command1', ['1any_arg1', '1any_arg2'], 'any_stdin')
            self.assertRaises(AssertionError, veri.verify, 'other_command', ['2any_arg1', '2any_arg2'], 'any_stdin2')

        self.assertEquals(call('/hello/world/test-execution/recorded-calls'), deserialize_mock.call_args)

    @patch('shtub.verifier.deserialize_stub_executions')
    def test_should_verify_all_recorded_calls_when_all_recorded_calls_fit_expectation (self, deserialize_mock):
        verifier = Verifier('/hello/world')
        
        stub_execution1 = Execution('any_command1', ['1any_arg1', '1any_arg2'], 'any_stdin1')
        stub_execution2 = Execution('any_command2', ['2any_arg1', '2any_arg2'], 'any_stdin2')
        
        deserialize_mock.return_value = [stub_execution1, stub_execution2]
        
        with verifier as veri:
            veri.verify('any_command1', ['1any_arg1', '1any_arg2'], 'any_stdin1')
            veri.verify('any_command2', ['2any_arg1', '2any_arg2'], 'any_stdin2')
            self.assertEqual(0, len(veri.recorded_calls))

        self.assertEquals(call('/hello/world/test-execution/recorded-calls'), deserialize_mock.call_args)
