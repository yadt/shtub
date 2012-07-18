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

from mock import Mock, call, patch

from StringIO import StringIO

from shtub import serialize_stub_executions, deserialize_stub_executions, deserialize_expectations
from shtub.answer import Answer
from shtub.execution import Execution
from shtub.expectation import Expectation


class IntegrationtestsTests (unittest.TestCase):
    @patch('json.loads')
    @patch('__builtin__.open')
    def test_should_deserialize_stub_executions (self, mock_open, mock_json):
        fake_file = self.return_file_when_calling(mock_open)
        executions = [Execution('command', ['-arg1', '-arg2', '-arg3'], 'stdin')]
        json_string = "[{'command': 'command', 'arguments': ['-arg1', '-arg2', '-arg3'], 'stdin': 'stdin'}]"
        fake_file.read.return_value = json_string
        mock_json.return_value = [{'command'   : 'command',
                                   'arguments' : ['-arg1', '-arg2', '-arg3'],
                                   'stdin'     : 'stdin'}]
                
        actual_executions = deserialize_stub_executions('executions.json')
        
        self.assertEquals(call('executions.json', 'r'), mock_open.call_args)
        self.assertEquals(call(), fake_file.read.call_args)
        self.assertEquals(call(json_string), mock_json.call_args)
        
        expected_executions = [Execution('command', ['-arg1', '-arg2', '-arg3'], 'stdin')]
        self.assertEquals(expected_executions, actual_executions)

    @patch('json.loads')
    @patch('__builtin__.open')
    def test_should_deserialize_expectations (self, mock_open, mock_json):
        fake_file = self.return_file_when_calling(mock_open)
        executions = [Expectation('command', ['-arg1', '-arg2', '-arg3'], 'stdin')]
        json_string = "[{'command': 'command', 'arguments': ['-arg1', '-arg2', '-arg3'], 'stdin': 'stdin', 'current_answer': 0, 'answers': []} ]"
        fake_file.read.return_value = json_string
        mock_json.return_value = [{'command'        : 'command',
                                   'arguments'      : ['-arg1', '-arg2', '-arg3'],
                                   'stdin'          : 'stdin',
                                   'current_answer' : 0,
                                   'answers'        : [{'stdout'      : 'stdout',
                                                        'stderr'      : 'stderr',
                                                        'return_code' : 15}]
                                 }]
                
        actual_expectations = deserialize_expectations('executions.json')
        
        self.assertEquals(call('executions.json', 'r'), mock_open.call_args)
        self.assertEquals(call(), fake_file.read.call_args)
        self.assertEquals(call(json_string), mock_json.call_args)
        
        expected_expectations = [Expectation('command', ['-arg1', '-arg2', '-arg3'], 'stdin', [Answer('stdout', 'stderr', 15)], 0)]
        
        self.assertEquals(expected_expectations, actual_expectations)

    @patch('json.dumps')
    @patch('__builtin__.open')
    def test_should_serialize_stub_executions (self, mock_open, mock_json):
        fake_file = self.return_file_when_calling(mock_open)
        mock_json.return_value = '[{"some": "json"}]'
        executions = [Execution('command', ['-arg1', '-arg2', '-arg3'], 'stdin')]

        serialize_stub_executions('executions.json', executions)
        
        expected_dictionary = {'command'   : 'command', 
                               'arguments' : ['-arg1', '-arg2', '-arg3'], 
                               'stdin'     : 'stdin'}
        
        self.assertEquals(call([expected_dictionary], sort_keys=True, indent=4), mock_json.call_args)
        self.assertEquals(call('executions.json', 'w'), mock_open.call_args)
        self.assertEquals(call('[{"some": "json"}]'), fake_file.write.call_args)

    def return_file_when_calling (self, mock_open, content=None):
        file_handle = Mock()
        
        mock_open.return_value.__enter__ = Mock(return_value=file_handle)
        mock_open.return_value.__exit__ = Mock()
        
        if content is not None:
            mock_open.return_value.read.return_value = content
        
        return file_handle
