import logging
import sys

from mock import Mock, patch, call, ANY
from StringIO import StringIO

from shtub import commandstub, BASEDIR, LOG_FILENAME
from shtub.answer import Answer
from shtub.execution import Execution
from shtub.expectation import Expectation
from shtub.testbase import TestCase

class CommandStubTests (TestCase):
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
        
        record_mock.assert_called_once_with(execution)
        answer_mock.assert_called_once_with(answer)
        
    @patch('sys.exit')
    @patch('logging.error')
    @patch('logging.info')
    @patch('shtub.commandstub.deserialize_expectations', return_value=[])
    def test_should_exit_with_error_code_255_when_execution_not_in_expectation (self, \
                                            deserialize_mock, info_mock, error_mock, exit_mock):
        
        execution = Execution('command', ['-arg1', '-arg2', '-arg3'], 'stdin')
        
        commandstub.dispatch(execution)
        
        exit_mock.assert_called_once_with(255)
        
    @patch('sys.exit')
    @patch('logging.error')
    @patch('logging.info')
    @patch('shtub.commandstub.deserialize_expectations', return_value=[])
    def test_should_load_expectations (self, deserialize_mock, info_mock, error_mock, exit_mock):
        execution = Execution('command', ['-arg1', '-arg2', '-arg3'], 'stdin')
        
        commandstub.dispatch(execution)
        
        deserialize_mock.assert_called_once_with('test-execution/expectations')
        
    
    @patch('shtub.commandstub.serialize_stub_executions')
    @patch('shtub.commandstub.deserialize_stub_executions', return_value=[])
    @patch('os.path.exists', return_value=True)
    def test_should_append_execution_and_serialize (self, exists_mock, deserialize_mock, serialize_mock):
        execution = Execution('command', ['-arg1', '-arg2', '-arg3'], 'stdin')
        
        commandstub.record_call(execution)
        
        serialize_mock.assert_called_once_with('test-execution/recorded-calls', ANY)
        
        actual_recorded_calls = serialize_mock.call_args[0][1]
        
        self.assertEquals(str(execution), str(actual_recorded_calls[0]))

    @patch('shtub.commandstub.serialize_stub_executions')
    @patch('shtub.commandstub.deserialize_stub_executions')
    @patch('os.path.exists', return_value=True)
    def test_should_deserialize_when_file_exists (self, exists_mock, deserialize_mock, serialize_mock):
        execution = Execution('command', ['-arg1', '-arg2', '-arg3'], 'stdin')
        
        commandstub.record_call(execution)
        
        deserialize_mock.assert_called_once_with('test-execution/recorded-calls')

    @patch('shtub.commandstub.serialize_stub_executions')
    @patch('shtub.commandstub.deserialize_stub_executions')
    @patch('os.path.exists', return_value=False)
    def test_should_not_deserialize_when_file_does_not_exist (self, exists_mock, deserialize_mock, serialize_mock):
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
        exit_mock.assert_called_once_with(223)

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('sys.exit')
    def test_should_send_answer_without_writing_to_stdout_and_stderr (self, exit_mock, stderr_mock, stdout_mock):
        answer= Answer(None, None, 123)
        
        commandstub.send_answer(answer)
        
        self.assertEquals('', stdout_mock.getvalue())
        self.assertEquals('', stderr_mock.getvalue())
        exit_mock.assert_called_once_with(123)


    @patch('sys.stdin')
    @patch('shtub.commandstub.select', return_value=([],[],[]))
    def test_should_use_a_one_second_timeout_when_waiting_for_stdin (self, select_mock, stdin_mock):
        commandstub.read_stdin()
        
        select_mock.assert_called_once_with([sys.stdin], [], [], 1)

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
        
        exists_mock.assert_called_once_with('test-execution')
        mkdir_mock.assert_called_once_with('test-execution')

    @patch.object(sys, 'argv', ['command', '-arg1', '-arg2', '-arg3'])
    @patch('shtub.commandstub.read_stdin', return_value=None)
    @patch('shtub.commandstub.dispatch')
    @patch('logging.basicConfig')
    @patch('os.mkdir')
    @patch('os.path.exists', return_value = True)
    def test_should_not_create_basedir_if_already_exist (self, \
            exists_mock, mkdir_mock, logging_mock, dispatch_mock, read_stdin_mock):
        
        commandstub.handle_stub_call()
        
        
        exists_mock.assert_called_once_with('test-execution')
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
        
        logging_mock.assert_called_once_with(filename = LOG_FILENAME,
                                             level    = logging.INFO,
                                             format   = '%(asctime)s %(levelname)5s [%(name)s] - %(message)s')

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
