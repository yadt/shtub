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

import unittest

from mock import patch, call

from shtub.verifier import Verifier, VerfiableExecutionWrapper, VerificationException
from shtub.execution import Execution


class VerfierTest (unittest.TestCase):
    def test_should_create_object_with_given_base_dir (self):
        actual_verifier = Verifier('/abc/def')
        
        self.assertEqual('/abc/def', actual_verifier.base_dir)


    def test_should_initialize_recoreded_calls (self):
        actual_verifier = Verifier('/abc/def')

        self.assertEqual([], actual_verifier.recorded_calls)


    @patch('os.path.exists')
    def test_should_raise_exception_when_recorded_calls_file_does_not_exist (self, mock_exists):
        mock_exists.return_value = False
        verifier = Verifier('/spam/eggs')
        
        self.assertRaises(VerificationException, verifier.__enter__)
        self.assertEqual(call('/spam/eggs/shtub/executions'), mock_exists.call_args)


    @patch('os.path.exists')
    @patch('shtub.verifier.deserialize_executions')
    def test_should_deserialize_recorded_calls_and_return_verifier_itself_when_entering_with_statement (self, mock_deserialize, mock_exists):
        mock_exists.return_value = True
        verifier = Verifier('/hello/world')
                
        with verifier as veri:
            self.assertEqual(veri, verifier)
            
        self.assertEqual(call('/hello/world/shtub/executions'), mock_deserialize.call_args)


    @patch('os.path.exists')
    @patch('shtub.verifier.deserialize_executions')
    def test_should_raise_exception_when_no_executed_calls_recorded (self, mock_deserialize, mock_exists):
        mock_exists.return_value = True
        verifier = Verifier('/hello/world')
        
        mock_deserialize.return_value = []
        
        with verifier as veri:
            self.assertRaises(AssertionError, veri.verify, 'any_stub', ['any_arguments'], 'any_stdin')

        self.assertEqual(call('/hello/world/shtub/executions'), mock_deserialize.call_args)


    @patch('os.path.exists')
    @patch('shtub.verifier.deserialize_executions')
    def test_should_raise_exception_when_recorded_call_does_not_fit_expectation (self, mock_deserialize, mock_exists):
        mock_exists.return_value = True
        verifier = Verifier('/hello/world')
        
        stub_execution = Execution('any_command', ['any_arg1', 'any_arg2'], 'any_stdin', expected=True)
        
        mock_deserialize.return_value = [stub_execution]
        
        verify = verifier.__enter__()
        self.assertRaises(AssertionError, verify.verify, 'other_command', ['any_arg1', 'any_arg2'], 'any_stdin')
        self.assertEqual(call('/hello/world/shtub/executions'), mock_deserialize.call_args)


    @patch('os.path.exists')
    @patch('shtub.verifier.deserialize_executions')
    def test_should_raise_exception_when_second_recorded_call_does_not_fit_expectation (self, mock_deserialize, mock_exists):
        mock_exists.return_value = True
        verifier = Verifier('/hello/world')
        
        stub_execution1 = Execution('any_command1', ['1any_arg1', '1any_arg2'], 'any_stdin', expected=True)
        stub_execution2 = Execution('any_command2', ['2any_arg1', '2any_arg2'], 'any_stdin2', expected=True)
        
        mock_deserialize.return_value = [stub_execution1, stub_execution2]
        
        verify = verifier.__enter__()
        verify.verify('any_command1', ['1any_arg1', '1any_arg2'], 'any_stdin')
        
        self.assertRaises(AssertionError, verify.verify, 'other_command', ['2any_arg1', '2any_arg2'], 'any_stdin2')
        self.assertEqual(call('/hello/world/shtub/executions'), mock_deserialize.call_args)


    @patch('os.path.exists')
    @patch('shtub.verifier.deserialize_executions')
    def test_should_verify_all_recorded_calls_when_all_recorded_calls_fit_expectation (self, mock_deserialize, mock_exists):
        mock_exists.return_value = True
        verifier = Verifier('/hello/world')
        
        stub_execution1 = Execution('any_command1', ['1any_arg1', '1any_arg2'], 'any_stdin1', expected=True)
        stub_execution2 = Execution('any_command2', ['2any_arg1', '2any_arg2'], 'any_stdin2', expected=True)
        
        mock_deserialize.return_value = [stub_execution1, stub_execution2]
        
        with verifier as veri:
            veri.verify('any_command1', ['1any_arg1', '1any_arg2'], 'any_stdin1')
            veri.verify('any_command2', ['2any_arg1', '2any_arg2'], 'any_stdin2')
            self.assertEqual(0, len(veri.recorded_calls))

        self.assertEqual(call('/hello/world/shtub/executions'), mock_deserialize.call_args)


    @patch('os.path.exists')
    @patch('shtub.verifier.deserialize_executions')
    def test_should_raise_exception_when_execution_has_not_been_accepted (self, mock_deserialize, mock_exists):
        mock_exists.return_value = True
        verifier = Verifier('/hello/world')
        
        stub_execution1 = Execution('any_command1', ['1any_arg1', '1any_arg2'], 'any_stdin1')
        
        mock_deserialize.return_value = [stub_execution1]
        
        self.assertRaises(VerificationException, verifier.__enter__)


    @patch('os.path.exists')
    @patch('shtub.verifier.deserialize_executions')
    def test_should_raise_exception_when_the_second_execution_has_not_been_accepted (self, mock_deserialize, mock_exists):
        mock_exists.return_value = True
        verifier = Verifier('/hello/world')
        
        stub_execution1 = Execution('any_command1', ['1any_arg1', '1any_arg2'], 'any_stdin1', expected=True)
        stub_execution2 = Execution('any_command2', ['2any_arg1', '2any_arg2'], 'any_stdin2')
        
        mock_deserialize.return_value = [stub_execution1, stub_execution2]
        
        self.assertRaises(VerificationException, verifier.__enter__)


    @patch('os.path.exists')
    @patch('shtub.verifier.deserialize_executions')
    def test_should_verify_command_has_been_called (self, mock_deserialize, mock_exists):
        mock_exists.return_value = True
        verifier = Verifier('/hello/world')
        
        stub_execution = Execution('command', ['-arg1', '-arg2'], 'stdin', expected=True)
        
        mock_deserialize.return_value = [stub_execution]
        
        with verifier as verify:
            called_command = verify.called('command')
            self.assertEqual(called_command.execution, stub_execution)
            self.assertEqual(0, len(verify.recorded_calls))

        self.assertEqual(call('/hello/world/shtub/executions'), mock_deserialize.call_args)


    @patch('os.path.exists')
    @patch('shtub.verifier.deserialize_executions')
    def test_should_raise_exception_when_expected_command_has_not_been_executed (self, mock_deserialize, mock_exists):
        mock_exists.return_value = True
        verifier = Verifier('/hello/world')
        
        stub_execution = Execution('command', ['-arg1', '-arg2'], 'stdin', expected=True)
        
        mock_deserialize.return_value = [stub_execution]

        verify = verifier.__enter__()
        self.assertRaises(AssertionError, verifier.called, 'other_command')


    @patch('os.path.exists')
    @patch('shtub.verifier.deserialize_executions')
    def test_should_raise_exception_when_no_recorded_calls_available (self, mock_deserialize, mock_exists):
        mock_exists.return_value = True
        verifier = Verifier('/hello/world')
        
        mock_deserialize.return_value = []

        with verifier as verify:
            self.assertRaises(AssertionError, verifier.called, 'other_command')


    @patch('os.path.exists')
    @patch('shtub.verifier.deserialize_executions')
    def test_should_raise_exception_when_more_recorded_calls_available_than_verified (self, mock_deserialize, mock_exists):
        mock_exists.return_value = True
        verifier = Verifier('/hello/world')
        
        stub_execution1 = Execution('command', ['-arg1', '-arg2'], 'stdin', expected=True)
        stub_execution2 = Execution('command', ['-arg1', '-arg2'], 'stdin', expected=True)
        
        mock_deserialize.return_value = [stub_execution1, stub_execution2]
        
        verify = verifier.__enter__()
        verify.called('command')
        self.assertRaises(VerificationException, verify.__exit__, None, None, None)


    @patch('os.path.exists')
    @patch('shtub.verifier.deserialize_executions')
    def test_should_return_false_when_an_exception_occured_in_the_with_statement (self, mock_deserialize, mock_exists):
        mock_exists.return_value = True
        verifier = Verifier('/hello/world')
        
        stub_execution1 = Execution('command', ['-arg1', '-arg2'], 'stdin', expected=True)
        stub_execution2 = Execution('command', ['-arg1', '-arg2'], 'stdin', expected=True)
        
        mock_deserialize.return_value = [stub_execution1, stub_execution2]
        
        verify = verifier.__enter__()
        verify.called('command')
        
        actual_result = verify.__exit__('exception_type', 'exception_value', 'traceback')
        
        self.assertFalse(actual_result)


class VerfiableExecutionWrapperTests (unittest.TestCase):
    def test_should_verify_at_least_given_argument (self):
        execution = Execution('command', ['-arg1', '-arg2', '-arg3'], 'stdin')
        wrapper = VerfiableExecutionWrapper(execution)
        
        actual_value = wrapper.at_least_with_arguments('-arg1')
        
        self.assertEqual(wrapper, actual_value)


    def test_should_verify_at_least_given_arguments (self):
        execution = Execution('command', ['-arg1', '-arg2', '-arg3'], 'stdin')
        wrapper = VerfiableExecutionWrapper(execution)
        
        actual_value = wrapper.at_least_with_arguments('-arg1', '-arg2')
        
        self.assertEqual(wrapper, actual_value)


    def test_should_raise_exception_when_given_argument_is_not_execution (self):
        execution = Execution('command', ['-arg1', '-arg2', '-arg3'], 'stdin')
        wrapper = VerfiableExecutionWrapper(execution)
        
        self.assertRaises(AssertionError, wrapper.at_least_with_arguments, '-arg0')


    def test_should_verify_given_arguments (self):
        execution = Execution('command', ['-arg1', '-arg2', '-arg3'], 'stdin')
        wrapper = VerfiableExecutionWrapper(execution)
        
        actual_value = wrapper.with_arguments('-arg1', '-arg2', '-arg3')
        
        self.assertEqual(wrapper, actual_value)


    def test_should_raise_exception_when_given_arguments_are_different (self):
        execution = Execution('command', ['-arg1', '-arg2', '-arg3'], 'stdin')
        wrapper = VerfiableExecutionWrapper(execution)
        
        self.assertRaises(AssertionError, wrapper.with_arguments, '-arg1', '-arg2', 'arg3')


    def test_should_verify_given_input (self):
        execution = Execution('command', ['-arg1', '-arg2', '-arg3'], 'stdin')
        wrapper = VerfiableExecutionWrapper(execution)
        
        actual_value = wrapper.with_input('stdin')
        
        self.assertEqual(wrapper, actual_value)


    def test_should_raise_exception_when_given_input_is_different (self):
        execution = Execution('command', ['-arg1', '-arg2', '-arg3'], 'stdin')
        wrapper = VerfiableExecutionWrapper(execution)
        
        self.assertRaises(AssertionError, wrapper.with_input, 'hello world')


    def test_should_verify_input_using_with_or_and (self):
        execution = Execution('command', ['-arg1', '-arg2', '-arg3'], 'stdin')
        wrapper = VerfiableExecutionWrapper(execution)
        
        self.assertEqual(wrapper.and_input, wrapper.with_input)

