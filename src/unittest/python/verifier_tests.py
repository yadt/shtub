#   shtub - shell command stub
#   Copyright (C) 2012-2013 Immobilien Scout GmbH
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

from shtub.verification.verifierloader import VerifierLoader, Verifier
from shtub.verification import VerificationException
from shtub.verification.commandinputverifier import CommandInputVerifier
from shtub.execution import Execution
from shtub.commandinput import CommandInput


class VerifierLoaderTest (unittest.TestCase):
    def test_should_create_object_with_given_base_dir (self):
        actual = VerifierLoader('/abc/def')
        
        self.assertEqual('/abc/def', actual.base_dir)


    def test_should_initialize_recoreded_calls (self):
        verifier = VerifierLoader('/abc/def')

        actual_executions = verifier.executions
        
        self.assertEqual([], actual_executions)


    @patch('os.path.exists')
    def test_should_raise_exception_when_recorded_calls_file_does_not_exist (self, mock_exists):
        mock_exists.return_value = False
        verifier = VerifierLoader('/spam/eggs')
        
        self.assertRaises(VerificationException, verifier.__enter__)
        self.assertEqual(call('/spam/eggs/shtub/executions'), mock_exists.call_args)


    @patch('os.path.exists')
    @patch('shtub.verification.verifierloader.deserialize_executions')
    def test_should_deserialize_recorded_calls_and_return_verifier_itself_when_entering_with_statement (self, mock_deserialize, mock_exists):
        mock_exists.return_value = True
        verifier = VerifierLoader('/hello/world')
                
        with verifier as veri:
            self.assertEqual(veri, verifier)
            
        self.assertEqual(call('/hello/world/shtub/executions'), mock_deserialize.call_args)


    @patch('os.path.exists')
    @patch('shtub.verification.verifierloader.deserialize_executions')
    def test_should_raise_exception_when_execution_has_not_been_accepted (self, mock_deserialize, mock_exists):
        mock_exists.return_value = True
        verifier = VerifierLoader('/hello/world')
        execution1 = Execution('any_command1', ['1any_arg1', '1any_arg2'], 'any_stdin1')
        mock_deserialize.return_value = [execution1]
        
        self.assertRaises(VerificationException, verifier.__enter__)


    @patch('os.path.exists')
    @patch('shtub.verification.verifierloader.deserialize_executions')
    def test_should_raise_exception_when_the_second_execution_has_not_been_accepted (self, mock_deserialize, mock_exists):
        mock_exists.return_value = True
        verifier = VerifierLoader('/hello/world')
        
        execution1 = Execution('any_command1', ['1any_arg1', '1any_arg2'], 'any_stdin1', expected=True)
        execution2 = Execution('any_command2', ['2any_arg1', '2any_arg2'], 'any_stdin2')
        
        mock_deserialize.return_value = [execution1, execution2]
        
        self.assertRaises(VerificationException, verifier.__enter__)

    @patch('os.path.exists')
    @patch('shtub.verification.verifierloader.deserialize_executions')
    def test_should_return_new_verifier_object(self, mock_deserialize, mock_exists):
        mock_exists.return_value = True
        mock_deserialize.return_value = []

        verifier = VerifierLoader('/hello/world')

        with verifier as verify:
            self.assertTrue(verify.filter_by_argument('foobar') is not verify, "should not return itself")


    @patch('os.path.exists')
    @patch('shtub.verification.verifierloader.deserialize_executions')
    def test_should_return_empty_verifier_when_filtering_by_argument_without_executions(self, mock_deserialize, mock_exists):
        mock_exists.return_value = True
        mock_deserialize.return_value = []

        verifier = VerifierLoader('/hello/world')

        with verifier as verify:
            with verify.filter_by_argument('foobar') as verify_foobar:

                self.assertEqual([], verify_foobar.executions)

    @patch('os.path.exists')
    @patch('shtub.verification.verifierloader.deserialize_executions')
    def test_should_return_verifier_with_one_matching_execution_when_filtering_by_argument(self, mock_deserialize, mock_exists):
        mock_exists.return_value = True
        execution1 = Execution('command', ['-arg1', '-arg2'], 'stdin', expected=True)
        mock_deserialize.return_value = [execution1]

        verifier = VerifierLoader('/hello/world')

        verify = verifier.__enter__()

        with verify.filter_by_argument('-arg1') as verify_foobar:
            self.assertEqual([execution1], verify_foobar.executions)
            verify_foobar.finished()

    @patch('os.path.exists')
    @patch('shtub.verification.verifierloader.deserialize_executions')
    def test_should_return_empty_verifier_when_filtering_by_argument_not_matching_execution(self, mock_deserialize, mock_exists):
        mock_exists.return_value = True
        execution1 = Execution('command', ['-arg1', '-arg2'], 'stdin', expected=True)
        mock_deserialize.return_value = [execution1]

        verifier = VerifierLoader('/hello/world')

        verify = verifier.__enter__()

        with verify.filter_by_argument('foobar') as verify_foobar:
            self.assertEqual([], verify_foobar.executions)
            verify_foobar.finished()

    @patch('os.path.exists')
    @patch('shtub.verification.verifierloader.deserialize_executions')
    def test_should_return_verifier_with_one_matching_execution_when_filtering_two_executions_by_argument(self, mock_deserialize, mock_exists):
        mock_exists.return_value = True
        execution1 = Execution('command', ['-arg1', '-arg2'], 'stdin', expected=True)
        execution2 = Execution('command', ['-arg2', '-arg3'], 'stdin', expected=True)
        mock_deserialize.return_value = [execution1, execution2]

        verifier = VerifierLoader('/hello/world')

        verify = verifier.__enter__()

        with verify.filter_by_argument('-arg1') as verify_foobar:
            self.assertEqual([execution1], verify_foobar.executions)
            verify_foobar.finished()

    @patch('os.path.exists')
    @patch('shtub.verification.verifierloader.deserialize_executions')
    def test_should_return_verifier_with_matching_executions_when_filtering_by_argument(self, mock_deserialize, mock_exists):
        mock_exists.return_value = True
        execution1 = Execution('command', ['-arg1', '-arg2'], 'stdin', expected=True)
        execution2 = Execution('command', ['-arg1', '-arg3'], 'stdin', expected=True)
        execution3 = Execution('command', ['-arg2', '-arg4'], 'stdin', expected=True)
        execution4 = Execution('command', ['-arg3', '-arg4'], 'stdin', expected=True)
        mock_deserialize.return_value = [execution1, execution2, execution3, execution4]

        verifier = VerifierLoader('/hello/world')

        verify = verifier.__enter__()

        with verify.filter_by_argument('-arg2') as verify_foobar:
            self.assertEqual([execution1, execution3], verify_foobar.executions)
            verify_foobar.finished()

    @patch('os.path.exists')
    @patch('shtub.verification.verifierloader.deserialize_executions')
    def test_should_verify_command_has_been_called (self, mock_deserialize, mock_exists):
        mock_exists.return_value = True
        verifier = VerifierLoader('/hello/world')

        stub_execution = Execution('command', ['-arg1', '-arg2'], 'stdin', expected=True)

        mock_deserialize.return_value = [stub_execution]

        with verifier as verify:
            called_command = verify.called('command')
            self.assertEqual(0, len(verify.executions))

        self.assertEqual(call('/hello/world/shtub/executions'), mock_deserialize.call_args)


class VerifierTests (unittest.TestCase):

    def test_should_initialize_with_empty_list_of_executions(self):
        verifier = Verifier([])

        self.assertEqual([], verifier.executions)

    def test_should_return_self(self):
        verifier = Verifier([])

        actual_object = verifier.__enter__()

        self.assertTrue(verifier is actual_object)


class CommandInputVerifierTests (unittest.TestCase):
    def test_should_verify_at_least_given_argument (self):
        command_input = CommandInput('command', ['-arg1', '-arg2', '-arg3'], 'stdin')
        wrapper = CommandInputVerifier(command_input)
        
        actual_value = wrapper.at_least_with_arguments('-arg1')
        
        self.assertEqual(wrapper, actual_value)


    def test_should_verify_at_least_given_arguments (self):
        command_input = CommandInput('command', ['-arg1', '-arg2', '-arg3'], 'stdin')
        wrapper = CommandInputVerifier(command_input)
        
        actual_value = wrapper.at_least_with_arguments('-arg1', '-arg2')
        
        self.assertEqual(wrapper, actual_value)


    def test_should_raise_exception_when_given_argument_is_not_execution (self):
        command_input = CommandInput('command', ['-arg1', '-arg2', '-arg3'], 'stdin')
        wrapper = CommandInputVerifier(command_input)
        
        self.assertRaises(VerificationException, wrapper.at_least_with_arguments, '-arg0')


    def test_should_verify_given_arguments (self):
        command_input = CommandInput('command', ['-arg1', '-arg2', '-arg3'], 'stdin')
        wrapper = CommandInputVerifier(command_input)
        
        actual_value = wrapper.with_arguments('-arg1', '-arg2', '-arg3')
        
        self.assertEqual(wrapper, actual_value)


    def test_should_raise_exception_when_given_arguments_are_different (self):
        command_input = CommandInput('command', ['-arg1', '-arg2', '-arg3'], 'stdin')
        wrapper = CommandInputVerifier(command_input)
        
        self.assertRaises(VerificationException, wrapper.with_arguments, '-arg1', '-arg2', 'arg3')


    def test_should_verify_given_input (self):
        command_input = CommandInput('command', ['-arg1', '-arg2', '-arg3'], 'stdin')
        wrapper = CommandInputVerifier(command_input)
        
        actual_value = wrapper.with_input('stdin')
        
        self.assertEqual(wrapper, actual_value)


    def test_should_raise_exception_when_given_input_is_different (self):
        command_input = CommandInput('command', ['-arg1', '-arg2', '-arg3'], 'stdin')
        wrapper = CommandInputVerifier(command_input)
        
        self.assertRaises(VerificationException, wrapper.with_input, 'hello world')


    def test_should_verify_input_using_with_or_and (self):
        command_input = CommandInput('command', ['-arg1', '-arg2', '-arg3'], 'stdin')
        wrapper = CommandInputVerifier(command_input)
        
        self.assertEqual(wrapper.and_input, wrapper.with_input)

    def test_should_raise_exception_when_no_argument_matches_given_string(self):
        command_input = CommandInput('command', ['arg1', 'arg2', 'arg3'], 'stdin')
        wrapper = CommandInputVerifier(command_input)

        self.assertRaises(VerificationException, wrapper.at_least_one_argument_matches, 'spameggs')

    def test_should_verify_argument_when_argument_equals_given_pattern(self):
        command_input = CommandInput('command', ['arg1'], 'stdin')
        wrapper = CommandInputVerifier(command_input)

        actual_value = wrapper.at_least_one_argument_matches('arg1')

        self.assertEqual(wrapper, actual_value)

    def test_should_verify_argument_when_argument_matches_given_pattern(self):
        command_input = CommandInput('command', ['arg1'], 'stdin')
        wrapper = CommandInputVerifier(command_input)

        actual_value = wrapper.at_least_one_argument_matches('^arg')

        self.assertEqual(wrapper, actual_value)

    def test_should_verify_arguments_when_at_least_one_argument_matches_given_pattern(self):
        command_input = CommandInput('command', ['arg1', 'borg', 'spam', 'eggs'], 'stdin')
        wrapper = CommandInputVerifier(command_input)

        actual_value = wrapper.at_least_one_argument_matches('.*pam$')

        self.assertEqual(wrapper, actual_value)

    def test_should_verify_more_complex_pattern_given(self):
        command_input = CommandInput('command', ['arg1', 'borg', 'spam', '123abc'], 'stdin')
        wrapper = CommandInputVerifier(command_input)

        actual_value = wrapper.at_least_one_argument_matches('\d{3}[a-c]{3}')

        self.assertEqual(wrapper, actual_value)

    def test_should_verify_at_least_one_argument_matches_using_and (self):
        command_input = CommandInput('command', ['-arg1', '-arg2', '-arg3'], 'stdin')
        wrapper = CommandInputVerifier(command_input)

        self.assertEqual(wrapper.and_at_least_one_argument_matches, wrapper.at_least_one_argument_matches)

    def test_should_pop_verified_execution (self):
        stub_execution = Execution('command', ['-arg1', '-arg2'], 'stdin', expected=True)
        verifier = Verifier([stub_execution])

        verifier.called('command')

        self.assertEqual(0, len(verifier.executions))

    def test_should_raise_exception_when_expected_command_has_not_been_executed (self):
        stub_execution = Execution('command', ['-arg1', '-arg2'], 'stdin', expected=True)
        verifier = Verifier([stub_execution])

        self.assertRaises(VerificationException, verifier.called, 'other_command')

    def test_should_raise_exception_when_no_recorded_calls_available (self):
        verifier = Verifier([])

        self.assertRaises(VerificationException, verifier.called, 'other_command')

    def test_should_raise_exception_when_one_more_recorded_calls_available_than_verified (self):
        execution1 = Execution('command', ['-arg1', '-arg2'], 'stdin', expected=True)
        execution2 = Execution('command', ['-arg1', '-arg2'], 'stdin', expected=True)
        verifier = Verifier([execution1, execution2])

        verifier.called('command')

        self.assertRaises(VerificationException, verifier.__exit__, None, None, None)

    def test_should_raise_exception_when_more_recorded_calls_available_than_verified (self):
        execution1 = Execution('command', ['-arg1', '-arg2'], 'stdin', expected=True)
        execution2 = Execution('command', ['-arg1', '-arg2'], 'stdin', expected=True)
        execution3 = Execution('command', ['-arg1', '-arg2'], 'stdin', expected=True)
        verifier = Verifier([execution1, execution2, execution3])

        verifier.called('command')

        self.assertRaises(VerificationException, verifier.__exit__, None, None, None)

    def test_should_return_false_when_an_exception_occured_in_the_with_statement (self):
        execution1 = Execution('command', ['-arg1', '-arg2'], 'stdin', expected=True)
        execution2 = Execution('command', ['-arg1', '-arg2'], 'stdin', expected=True)
        verifier = Verifier([execution1, execution2])

        verifier.called('command')
        actual_result = verifier.__exit__('exception_type', 'exception_value', 'traceback')

        self.assertFalse(actual_result)

    def test_should_not_raise_verification_exception_when_not_verifying_anything_else(self):
        execution1 = Execution('command', ['-arg1', '-arg2'], 'stdin', expected=True)
        execution2 = Execution('command', ['-arg1', '-arg2'], 'stdin', expected=True)
        verifier = Verifier([execution1, execution2])

        with verifier as verify:
            verify.finished()

