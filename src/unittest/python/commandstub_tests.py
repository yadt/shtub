import unittest2
import logging
import sys

from mock import Mock, patch, call, ANY
from StringIO import StringIO

from shtub import commandstub, BASEDIR, LOG_FILENAME
from shtub.answer import Answer
from shtub.execution import Execution
from shtub.expectation import Expectation

class Tests (unittest2.TestCase):
    @patch('shtub.commandstub.record_call')
    @patch('shtub.commandstub.send_answer')
    @patch('logging.info')
    @patch('shtub.commandstub.deserialize_expectations')
    def test_should_record_call_and_send_answer_when_execution_fulfills_expectations (self, \
                                            deserialize_mock, info_mock, answer_mock, record_mock):
        
        answer = Answer('Hello world', 'Hello error', 15)
        expectation = Expectation('command', ['-arg1', '-arg2', '-arg3'], 'stdin')
        expectation.then(answer)
        deserialize_mock.return_value = [expectation]
        
        execution = Execution('command', ['-arg1', '-arg2', '-arg3'], 'stdin')
        
        commandstub.dispatch(execution)
        
        self.assertEquals(call(execution), record_mock.call_args)
        self.assertEquals(call(answer), answer_mock.call_args)
        
    @patch('sys.exit')
    @patch('logging.error')
    @patch('logging.info')
    @patch('shtub.commandstub.deserialize_expectations', return_value=[])
    def test_should_exit_with_error_code_255_when_execution_not_in_expectation (self, \
                                            deserialize_mock, info_mock, error_mock, exit_mock):
        
        execution = Execution('command', ['-arg1', '-arg2', '-arg3'], 'stdin')
        
        commandstub.dispatch(execution)
        
        self.assertEquals(call(255), exit_mock.call_args)
        
    @patch('sys.exit')
    @patch('logging.error')
    @patch('logging.info')
    @patch('shtub.commandstub.deserialize_expectations', return_value=[])
    def test_should_load_expectations (self, deserialize_mock, info_mock, error_mock, exit_mock):
        execution = Execution('command', ['-arg1', '-arg2', '-arg3'], 'stdin')
        
        commandstub.dispatch(execution)
        
        self.assertEquals(call('test-execution/expectations'), deserialize_mock.call_args)
        
    @patch('shtub.commandstub.unlock')
    @patch('shtub.commandstub.lock')
    @patch('shtub.commandstub.serialize_stub_executions')
    @patch('shtub.commandstub.deserialize_stub_executions', return_value=[])
    @patch('os.path.exists', return_value=True)
    def test_should_append_execution_and_serialize (self, \
            exists_mock, deserialize_mock, serialize_mock, lock_mock, unlock_mock):
        execution = Execution('command', ['-arg1', '-arg2', '-arg3'], 'stdin')
        
        commandstub.record_call(execution)
        
        self.assertEquals(call('test-execution/recorded-calls', ANY), serialize_mock.call_args)
        
        actual_recorded_calls = serialize_mock.call_args[0][1]
        
        self.assertEquals(str(execution), str(actual_recorded_calls[0]))

    @patch('shtub.commandstub.unlock')
    @patch('shtub.commandstub.lock')
    @patch('shtub.commandstub.serialize_stub_executions')
    @patch('shtub.commandstub.deserialize_stub_executions')
    @patch('os.path.exists', return_value=True)
    def test_should_deserialize_when_file_exists (self, \
            exists_mock, deserialize_mock, serialize_mock, lock_mock, unlock_mock):
        execution = Execution('command', ['-arg1', '-arg2', '-arg3'], 'stdin')
        
        commandstub.record_call(execution)
        
        self.assertEquals(call('test-execution/recorded-calls'), deserialize_mock.call_args)

    @patch('shtub.commandstub.unlock')
    @patch('shtub.commandstub.lock')
    @patch('shtub.commandstub.serialize_stub_executions')
    @patch('shtub.commandstub.deserialize_stub_executions')
    @patch('os.path.exists', return_value=False)
    def test_should_not_deserialize_when_file_does_not_exist (self, \
                exists_mock, deserialize_mock, serialize_mock, lock_mock, unlock_mock):
        execution = Execution('command', ['-arg1', '-arg2', '-arg3'], 'stdin')
        
        commandstub.record_call(execution)
        
        self.assertIsNone(deserialize_mock.call_args)


    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('sys.exit')
    def test_should_send_answer (self, exit_mock, stderr_mock, stdout_mock):
        answer= Answer('Hello world!', 'Hello error!', 223)
        
        commandstub.send_answer(answer)
        
        self.assertEquals('Hello world!', stdout_mock.getvalue())
        self.assertEquals('Hello error!', stderr_mock.getvalue())
        self.assertEquals(call(223), exit_mock.call_args)

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('sys.exit')
    def test_should_send_answer_without_writing_to_stdout_and_stderr (self, exit_mock, stderr_mock, stdout_mock):
        answer= Answer(None, None, 123)
        
        commandstub.send_answer(answer)
        
        self.assertEquals('', stdout_mock.getvalue())
        self.assertEquals('', stderr_mock.getvalue())
        self.assertEquals(call(123), exit_mock.call_args)


    @patch('sys.stdin')
    @patch('shtub.commandstub.select', return_value=([],[],[]))
    def test_should_use_a_one_second_timeout_when_waiting_for_stdin (self, select_mock, stdin_mock):
        commandstub.read_stdin()
        
        self.assertEquals(call([sys.stdin], [], [], 1), select_mock.call_args)

    @patch('sys.stdin')
    @patch('shtub.commandstub.select', return_value=([],[],[]))
    def test_should_return_None_when_no_input_from_stdin (self, select_mock, stdin_mock):
        actual = commandstub.read_stdin()
        
        self.assertIsNone(actual)

    @patch('sys.stdin')
    @patch('shtub.commandstub.select')
    def test_should_return_input_from_stdin (self, select_mock, stdin_mock):
        select_mock.return_value = ([StringIO('Hello world')], [], [])

        actual = commandstub.read_stdin()
        
        self.assertEquals('Hello world', actual)


    @patch.object(sys, 'argv', ['command', '-arg1', '-arg2', '-arg3'])
    @patch('shtub.commandstub.read_stdin', return_value=None)
    @patch('shtub.commandstub.dispatch')
    @patch('logging.basicConfig')
    @patch('os.mkdir')
    @patch('os.path.exists', return_value = False)
    def test_should_create_basedir_if_does_not_exist (self, \
            exists_mock, mkdir_mock, logging_mock, dispatch_mock, read_stdin_mock):
        
        commandstub.handle_stub_call()
        
        self.assertEquals(call('test-execution'), exists_mock.call_args)
        self.assertEquals(call('test-execution'), mkdir_mock.call_args)

    @patch.object(sys, 'argv', ['command', '-arg1', '-arg2', '-arg3'])
    @patch('shtub.commandstub.read_stdin', return_value=None)
    @patch('shtub.commandstub.dispatch')
    @patch('logging.basicConfig')
    @patch('os.mkdir')
    @patch('os.path.exists', return_value = True)
    def test_should_not_create_basedir_if_already_exist (self, \
            exists_mock, mkdir_mock, logging_mock, dispatch_mock, read_stdin_mock):
        
        commandstub.handle_stub_call()
        
        
        self.assertEquals(call('test-execution'), exists_mock.call_args)
        self.assertIsNone(mkdir_mock.call_args)

    @patch.object(sys, 'argv', ['command', '-arg1', '-arg2', '-arg3'])
    @patch('shtub.commandstub.read_stdin', return_value=None)
    @patch('shtub.commandstub.dispatch')
    @patch('logging.basicConfig')
    @patch('os.mkdir')
    @patch('os.path.exists', return_value = True)
    def test_should_initialize_basic_logging_configuration (self, \
            exists_mock, mkdir_mock, logging_mock, dispatch_mock, read_stdin_mock):
        
        commandstub.handle_stub_call()
        
        self.assertEquals(call(filename = LOG_FILENAME,
                               level    = logging.INFO,
                               format   = '%(asctime)s %(levelname)5s [%(name)s] - %(message)s'),
                          logging_mock.call_args)

    @patch.object(sys, 'argv', ['command', '-arg1', '-arg2', '-arg3'])
    @patch('shtub.commandstub.read_stdin', return_value=None)
    @patch('shtub.commandstub.dispatch')
    @patch('logging.basicConfig')
    @patch('os.mkdir')
    @patch('os.path.exists', return_value = True)
    def test_should_dispatch_execution (self, \
            exists_mock, mkdir_mock, logging_mock, dispatch_mock, read_stdin_mock):
        
        commandstub.handle_stub_call()
        
        dispatch_mock.assert_called()
        
        expected_execution = str(Execution('command', ['-arg1', '-arg2', '-arg3'], stdin=None))
        actual_execution = str(dispatch_mock.call_args[0][0])
        
        self.assertEquals(expected_execution, actual_execution)

    @patch('shtub.commandstub.fcntl')
    @patch('__builtin__.open')
    def test_should_create_lock (self, open_mock, fcntl_mock):
        fcntl_mock.LOCK_EX = 'LOCK_EX'
        file_handle_mock = Mock()
        open_mock.return_value = file_handle_mock
        
        actual_file_handle = commandstub.lock()
        
        self.assertEquals(file_handle_mock, actual_file_handle)
        self.assertEquals(call('test-execution/LOCK', 'a'), open_mock.call_args)
        self.assertEquals(call(file_handle_mock, fcntl_mock.LOCK_EX), fcntl_mock.flock.call_args)
    
    def test_should_unlock (self):
        file_handle_mock = Mock()
        
        commandstub.unlock(file_handle_mock)
        
        self.assertEquals(call(), file_handle_mock.close.call_args)
    
