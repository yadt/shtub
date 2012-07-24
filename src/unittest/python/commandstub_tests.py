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

import unittest2
import logging
import sys

from mock import ANY, Mock, call, patch 
from StringIO import StringIO

from shtub import BASEDIR, LOG_FILENAME, commandstub
from shtub.answer import Answer
from shtub.execution import Execution
from shtub.expectation import Expectation

class Tests (unittest2.TestCase):
    @patch('shtub.commandstub.record_call')
    @patch('shtub.commandstub.send_answer')
    @patch('logging.info')
    @patch('shtub.commandstub.deserialize_expectations')
    def test_should_record_call_and_send_answer_when_execution_fulfills_expectations (self, \
                        mock_deserialize, mock_logging_info, mock_answer, mock_record):
        
        answer = Answer('Hello world', 'Hello error', 15)
        expectation = Expectation('command', ['-arg1', '-arg2', '-arg3'], 'stdin')
        expectation.then(answer)
        mock_deserialize.return_value = [expectation]
        
        execution = Execution('command', ['-arg1', '-arg2', '-arg3'], 'stdin')
        
        commandstub.dispatch(execution)
        
        self.assertEquals(call(execution), mock_record.call_args)
        self.assertEquals(call(answer), mock_answer.call_args)
        
    @patch('sys.exit')
    @patch('logging.error')
    @patch('logging.info')
    @patch('shtub.commandstub.deserialize_expectations', return_value=[])
    def test_should_exit_with_error_code_255_when_execution_not_in_expectation (self, \
                        mock_deserialize, mock_logging_info, mock_logging_error, mock_exit):
        
        execution = Execution('command', ['-arg1', '-arg2', '-arg3'], 'stdin')
        
        commandstub.dispatch(execution)
        
        self.assertEquals(call(255), mock_exit.call_args)
        
    @patch('sys.exit')
    @patch('logging.error')
    @patch('logging.info')
    @patch('shtub.commandstub.deserialize_expectations', return_value=[])
    def test_should_load_expectations (self, \
                        mock_deserialize, mock_logging_info, mock_logging_error, mock_exit):
        execution = Execution('command', ['-arg1', '-arg2', '-arg3'], 'stdin')
        
        commandstub.dispatch(execution)
        
        self.assertEquals(call('test-execution/expectations'), mock_deserialize.call_args)
        
    @patch('shtub.commandstub.unlock')
    @patch('shtub.commandstub.lock')
    @patch('shtub.commandstub.serialize_stub_executions')
    @patch('shtub.commandstub.deserialize_stub_executions', return_value=[])
    @patch('os.path.exists', return_value=True)
    def test_should_append_execution_and_serialize (self, \
                        mock_exists, mock_deserialize, mock_serialize, mock_lock, mock_unlock):
        execution = Execution('command', ['-arg1', '-arg2', '-arg3'], 'stdin')
        
        commandstub.record_call(execution)
        
        self.assertEquals(call('test-execution/recorded-calls', ANY), mock_serialize.call_args)
        
        actual_recorded_calls = mock_serialize.call_args[0][1]
        
        self.assertEquals(str(execution), str(actual_recorded_calls[0]))

    @patch('shtub.commandstub.unlock')
    @patch('shtub.commandstub.lock')
    @patch('shtub.commandstub.serialize_stub_executions')
    @patch('shtub.commandstub.deserialize_stub_executions')
    @patch('os.path.exists', return_value=True)
    def test_should_deserialize_when_file_exists (self, \
                        mock_exists, mock_deserialize, mock_serialize, mock_lock, mock_unlock):
        execution = Execution('command', ['-arg1', '-arg2', '-arg3'], 'stdin')
        
        commandstub.record_call(execution)
        
        self.assertEquals(call('test-execution/recorded-calls'), mock_deserialize.call_args)

    @patch('shtub.commandstub.unlock')
    @patch('shtub.commandstub.lock')
    @patch('shtub.commandstub.serialize_stub_executions')
    @patch('shtub.commandstub.deserialize_stub_executions')
    @patch('os.path.exists', return_value=False)
    def test_should_not_deserialize_when_file_does_not_exist (self, \
                        mock_exists, mock_deserialize, mock_serialize, mock_lock, mock_unlock):
        execution = Execution('command', ['-arg1', '-arg2', '-arg3'], 'stdin')
        
        commandstub.record_call(execution)
        
        self.assertIsNone(mock_deserialize.call_args)


    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('sys.exit')
    def test_should_send_answer (self, mock_exit, mock_stderr, mock_stdout):
        answer= Answer('Hello world!', 'Hello error!', 223)
        
        commandstub.send_answer(answer)
        
        self.assertEquals('Hello world!', mock_stdout.getvalue())
        self.assertEquals('Hello error!', mock_stderr.getvalue())
        self.assertEquals(call(223), mock_exit.call_args)

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('sys.exit')
    def test_should_send_answer_without_writing_to_stdout_and_stderr (self, \
                        mock_exit, mock_stderr, mock_stdout):
        answer= Answer(None, None, 123)
        
        commandstub.send_answer(answer)
        
        self.assertEquals('', mock_stdout.getvalue())
        self.assertEquals('', mock_stderr.getvalue())
        self.assertEquals(call(123), mock_exit.call_args)


    @patch('sys.stdin')
    @patch('shtub.commandstub.select', return_value=([],[],[]))
    def test_should_use_a_one_second_timeout_when_waiting_for_stdin (self, \
                        mock_select, mock_stdin):
        commandstub.read_stdin()
        
        self.assertEquals(call([sys.stdin], [], [], 1), mock_select.call_args)

    @patch('sys.stdin')
    @patch('shtub.commandstub.select', return_value=([],[],[]))
    def test_should_return_None_when_no_input_from_stdin (self, mock_select, mock_stdin):
        actual = commandstub.read_stdin()
        
        self.assertIsNone(actual)

    @patch('sys.stdin')
    @patch('shtub.commandstub.select')
    def test_should_return_input_from_stdin (self, mock_select, mock_stdin):
        mock_select.return_value = ([StringIO('Hello world')], [], [])

        actual = commandstub.read_stdin()
        
        self.assertEquals('Hello world', actual)


    @patch.object(sys, 'argv', ['command', '-arg1', '-arg2', '-arg3'])
    @patch('shtub.commandstub.read_stdin', return_value=None)
    @patch('shtub.commandstub.dispatch')
    @patch('logging.basicConfig')
    @patch('os.mkdir')
    @patch('os.path.exists', return_value = False)
    def test_should_create_basedir_if_does_not_exist (self, \
            mock_exists, mock_mkdir, mock_logging, mock_dispatch, mock_read_stdin):
        
        commandstub.handle_stub_call()
        
        self.assertEquals(call('test-execution'), mock_exists.call_args)
        self.assertEquals(call('test-execution'), mock_mkdir.call_args)

    @patch.object(sys, 'argv', ['command', '-arg1', '-arg2', '-arg3'])
    @patch('shtub.commandstub.read_stdin', return_value=None)
    @patch('shtub.commandstub.dispatch')
    @patch('logging.basicConfig')
    @patch('os.mkdir')
    @patch('os.path.exists', return_value = True)
    def test_should_not_create_basedir_if_already_exist (self, \
            mock_exists, mock_mkdir, mock_logging, mock_dispatch, mock_read_stdin):
        
        commandstub.handle_stub_call()
        
        
        self.assertEquals(call('test-execution'), mock_exists.call_args)
        self.assertIsNone(mock_mkdir.call_args)

    @patch.object(sys, 'argv', ['command', '-arg1', '-arg2', '-arg3'])
    @patch('shtub.commandstub.read_stdin', return_value=None)
    @patch('shtub.commandstub.dispatch')
    @patch('logging.basicConfig')
    @patch('os.mkdir')
    @patch('os.path.exists', return_value = True)
    def test_should_initialize_basic_logging_configuration (self, \
            mock_exists, mock_mkdir, mock_logging, mock_dispatch, mock_read_stdin):
        
        commandstub.handle_stub_call()
        
        self.assertEquals(call(filename = LOG_FILENAME,
                               level    = logging.INFO,
                               format   = '%(asctime)s %(levelname)5s [%(name)s] - %(message)s'),
                          mock_logging.call_args)

    @patch.object(sys, 'argv', ['command', '-arg1', '-arg2', '-arg3'])
    @patch('shtub.commandstub.read_stdin', return_value=None)
    @patch('shtub.commandstub.dispatch')
    @patch('logging.basicConfig')
    @patch('os.mkdir')
    @patch('os.path.exists', return_value = True)
    def test_should_dispatch_execution (self, \
            mock_exists, mock_mkdir, mock_logging, mock_dispatch, mock_read_stdin):
        
        commandstub.handle_stub_call()
        
        mock_dispatch.assert_called()
        
        expected_execution = str(Execution('command', ['-arg1', '-arg2', '-arg3'], stdin=None))
        actual_execution = str(mock_dispatch.call_args[0][0])
        
        self.assertEquals(expected_execution, actual_execution)

    @patch('shtub.commandstub.fcntl')
    @patch('__builtin__.open')
    def test_should_create_lock (self, mock_open, mock_fcntl):
        mock_fcntl.LOCK_EX = 'LOCK_EX'
        file_handle_mock = Mock()
        mock_open.return_value = file_handle_mock
        
        actual_file_handle = commandstub.lock()
        
        self.assertEquals(file_handle_mock, actual_file_handle)
        self.assertEquals(call('test-execution/lock', 'a'), mock_open.call_args)
        self.assertEquals(call(file_handle_mock, mock_fcntl.LOCK_EX), mock_fcntl.flock.call_args)
    
    def test_should_unlock (self):
        file_handle_mock = Mock()
        
        commandstub.unlock(file_handle_mock)
        
        self.assertEquals(call(), file_handle_mock.close.call_args)
    
