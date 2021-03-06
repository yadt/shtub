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

import sys
import unittest

from mock import Mock, call, patch

if sys.version_info[0] == 3:
    builtin_string = 'builtins'
else:
    builtin_string = '__builtin__'

from shtub import __version__, serialize_as_dictionaries, deserialize_executions, deserialize_stub_configurations, lock, unlock
from shtub.answer import Answer
from shtub.execution import Execution
from shtub.stubconfiguration import StubConfiguration


class ShtubTests (unittest.TestCase):

    def test_if_this_test_fails_maybe_you_have_shtub_installed_locally(self):
        self.assertEqual('${version}', __version__)

    @patch('json.loads')
    @patch(builtin_string + '.open')
    def test_should_deserialize_stub_configuration_with_no_answers(self, mock_open, mock_json):
        fake_file = self.return_file_when_calling(mock_open)
        json_string = "[{'expected': false, 'command_input': {'stdin': 'stdin', 'command': 'command', 'arguments': ['-arg1', '-arg2', '-arg3']}}]"
        fake_file.read.return_value = json_string
        mock_json.return_value = [{'command_input': {'command': 'command',
                                                     'arguments': ['-arg1', '-arg2', '-arg3'],
                                                     'stdin': 'stdin'},
                                   'expected': False}]

        actual_stub_configuration = deserialize_executions(
            'stub_configuration.json')

        self.assertEqual(
            call('stub_configuration.json', mode='r'), mock_open.call_args)
        self.assertEqual(call(), fake_file.read.call_args)
        self.assertEqual(call(json_string), mock_json.call_args)

        expected_stub_configuration = [
            Execution('command', ['-arg1', '-arg2', '-arg3'], 'stdin')]
        self.assertEqual(
            expected_stub_configuration, actual_stub_configuration)

    @patch('json.loads')
    @patch(builtin_string + '.open')
    def test_should_deserialize_stub_configurations(self, mock_open, mock_json):
        fake_file = self.return_file_when_calling(mock_open)
        json_string = "[{'current_answer': 0, 'answers': [{'return_code': 15, 'stderr': 'stderr', 'stdout': 'stdout', 'milliseconds_to_wait': None}], 'command_input': {'stdin': 'stdin', 'command': 'command', 'arguments': ['-arg1', '-arg2', '-arg3']}}]"
        fake_file.read.return_value = json_string
        mock_json.return_value = [
            {'command_input': {'command': 'command',
                               'arguments': ['-arg1', '-arg2', '-arg3'],
                               'stdin': 'stdin'},
             'current_answer': 0,
             'answers': [{'stdout': 'stdout',
                          'stderr': 'stderr',
                          'return_code': 15,
                          'milliseconds_to_wait': None}]
             }]

        actual_stub_configurations = deserialize_stub_configurations(
            'stub_configuration.json')

        self.assertEqual(
            call('stub_configuration.json', mode='r'), mock_open.call_args)
        self.assertEqual(call(), fake_file.read.call_args)
        self.assertEqual(call(json_string), mock_json.call_args)

        expected_stub_configurations = [
            StubConfiguration('command', ['-arg1', '-arg2', '-arg3'], 'stdin', [Answer('stdout', 'stderr', 15)], 0)]

        self.assertEqual(
            expected_stub_configurations, actual_stub_configurations)

    @patch('shtub.lock')
    @patch('shtub.unlock')
    @patch('json.dumps')
    @patch(builtin_string + '.open')
    def test_should_serialize_as_dictionaries(self, mock_open, mock_json, mock_unlock, mock_lock):
        fake_file = self.return_file_when_calling(mock_open)
        mock_json.return_value = '[{"some": "json"}]'
        stub_configuration = [
            Execution('command', ['-arg1', '-arg2', '-arg3'], 'stdin', expected=True)]

        serialize_as_dictionaries(
            'stub_configuration.json', stub_configuration)

        expected_dictionary = {'command_input': {'command': 'command',
                                                 'arguments': ['-arg1', '-arg2', '-arg3'],
                                                 'stdin': 'stdin'},
                               'expected': True}

        self.assertEqual(
            call([expected_dictionary], sort_keys=True, indent=4), mock_json.call_args)
        self.assertEqual(
            call('stub_configuration.json', mode='w'), mock_open.call_args)
        self.assertEqual(call('[{"some": "json"}]'), fake_file.write.call_args)

    def return_file_when_calling(self, mock_open, content=None):
        file_handle = Mock()

        mock_open.return_value.__enter__ = Mock(return_value=file_handle)
        mock_open.return_value.__exit__ = Mock()

        if content is not None:
            mock_open.return_value.read.return_value = content

        return file_handle

    @patch('shtub.fcntl')
    @patch(builtin_string + '.open')
    def test_should_create_lock(self, mock_open, mock_fcntl):
        mock_fcntl.LOCK_EX = 'LOCK_EX'
        file_handle_mock = Mock()
        mock_open.return_value = file_handle_mock

        actual_file_handle = lock()

        self.assertEqual(file_handle_mock, actual_file_handle)
        self.assertEqual(call('shtub/lock', mode='a'), mock_open.call_args)
        self.assertEqual(
            call(file_handle_mock, mock_fcntl.LOCK_EX), mock_fcntl.flock.call_args)

    @patch('shtub.os.mkdir')
    @patch('shtub.os.path.exists')
    @patch('shtub.fcntl')
    @patch(builtin_string + '.open')
    def test_should_create_base_dir_if_it_does_not_exist_when_locking(self, mock_open, mock_fcntl, mock_exists, mock_mkdir):
        mock_fcntl.LOCK_EX = 'LOCK_EX'
        mock_exists.return_value = False
        file_handle_mock = Mock()
        mock_open.return_value = file_handle_mock

        lock()

        self.assertEqual(call('shtub'), mock_mkdir.call_args)

    def test_should_unlock(self):
        file_handle_mock = Mock()

        unlock(file_handle_mock)

        self.assertEqual(call(), file_handle_mock.close.call_args)
