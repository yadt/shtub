import unittest

from mock import call, patch, Mock

from StringIO import StringIO

from shtub import serialize_stub_executions, deserialize_stub_executions, deserialize_expectations
from shtub.answer import Answer
from shtub.execution import Execution
from shtub.expectation import Expectation


class IntegrationtestsTests (unittest.TestCase):
    @patch('json.loads')
    @patch('__builtin__.open')
    def test_should_deserialize_stub_executions (self, open_mock, json_mock):
        fake_file = self.return_file_when_calling(open_mock)
        executions = [Execution('command', ['-arg1', '-arg2', '-arg3'], 'stdin')]
        json_string = "[{'command': 'command', 'arguments': ['-arg1', '-arg2', '-arg3'], 'stdin': 'stdin'}]"
        fake_file.read.return_value = json_string
        json_mock.return_value = [{'command': 'command',
                                   'arguments': ['-arg1', '-arg2', '-arg3'],
                                   'stdin': 'stdin'}]
                
        actual_executions = deserialize_stub_executions('executions.json')
        
        self.assertEquals(call('executions.json', 'r'), open_mock.call_args)
        self.assertEquals(call(), fake_file.read.call_args)
        self.assertEquals(call(json_string), json_mock.call_args)
        
        expected_executions = [Execution('command', ['-arg1', '-arg2', '-arg3'], 'stdin')]
        self.assertEquals(expected_executions, actual_executions)

    @patch('json.loads')
    @patch('__builtin__.open')
    def test_should_deserialize_expectations (self, open_mock, json_mock):
        fake_file = self.return_file_when_calling(open_mock)
        executions = [Expectation('command', ['-arg1', '-arg2', '-arg3'], 'stdin')]
        json_string = "[{'command': 'command', 'arguments': ['-arg1', '-arg2', '-arg3'], 'stdin': 'stdin', 'current_answer': 0, 'answers': []} ]"
        fake_file.read.return_value = json_string
        json_mock.return_value = [{'command'        : 'command',
                                   'arguments'      : ['-arg1', '-arg2', '-arg3'],
                                   'stdin'          : 'stdin',
                                   'current_answer' : 0,
                                   'answers'        : [{'stdout'      : 'stdout',
                                                        'stderr'      : 'stderr',
                                                        'return_code' : 15}]
                                 }]
                
        actual_expectations = deserialize_expectations('executions.json')
        
        self.assertEquals(call('executions.json', 'r'), open_mock.call_args)
        self.assertEquals(call(), fake_file.read.call_args)
        self.assertEquals(call(json_string), json_mock.call_args)
        
        expected_expectations = [Expectation('command', ['-arg1', '-arg2', '-arg3'], 'stdin', [Answer('stdout', 'stderr', 15)], 0)]
        
        self.assertEquals(expected_expectations, actual_expectations)

    @patch('json.dumps')
    @patch('__builtin__.open')
    def test_should_serialize_stub_executions (self, open_mock, json_mock):
        fake_file = self.return_file_when_calling(open_mock)
        json_mock.return_value = '[{"some": "json"}]'
        executions = [Execution('command', ['-arg1', '-arg2', '-arg3'], 'stdin')]

        serialize_stub_executions('executions.json', executions)
        
        expected_dictionary = {'command'   : 'command', 
                               'arguments' : ['-arg1', '-arg2', '-arg3'], 
                               'stdin'     : 'stdin'}
        
        self.assertEquals(call([expected_dictionary], sort_keys=True, indent=4), json_mock.call_args)
        self.assertEquals(call('executions.json', 'w'), open_mock.call_args)
        self.assertEquals(call('[{"some": "json"}]'), fake_file.write.call_args)

    def return_file_when_calling (self, open_mock, content=None):
        file_handle = Mock()
        
        open_mock.return_value.__enter__ = Mock(return_value=file_handle)
        open_mock.return_value.__exit__ = Mock()
        
        if content is not None:
            open_mock.return_value.read.return_value = content
        
        return file_handle
