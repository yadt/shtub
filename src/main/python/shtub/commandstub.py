#!/usr/bin/env python
#
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

"""
    the command stub.
"""

from __future__ import division
import logging
import os
import sys
import time

__author__ = 'Alexander Metzner, Michael Gruber, Udo Juettner'

from select import select

from shtub import (BASEDIR,
                   EXECUTIONS_FILENAME,
                   CONFIGURED_STUBS_FILENAME,
                   lock,
                   unlock,
                   LOG_FILENAME,
                   READ_STDIN_TIMEOUT_IN_SECONDS,
                   SERIALIZATION_LOCK_FILENAME,
                   deserialize_executions,
                   deserialize_stub_configurations,
                   serialize_as_dictionaries)

from shtub.execution import Execution
from shtub.commandinput import CommandInput

global lock_handle


def record_execution(execution):
    """
        loads the list of recent executions from the EXECUTIONS_FILENAME file,
        appends the given execution to the list, then writes the list back to
        the file again. To assure only one process is reading and writing the
        file a file lock is used.
    """

    lock_file_handle = lock()
    executions = []

    if os.path.exists(EXECUTIONS_FILENAME):
        executions = deserialize_executions(EXECUTIONS_FILENAME)

    executions.append(execution)
    serialize_as_dictionaries(EXECUTIONS_FILENAME, executions)
    logging.info('Recorded %s executions.', len(executions))

    unlock(lock_file_handle)


def send_answer(answer):
    """
        writes the stdout and stderr as given in the answer and performs a
        sys.exit with the given return_code.
    """

    logging.info('Sending %s', answer)

    if answer.stdout is not None:
        sys.stdout.write(answer.stdout)

    if answer.stderr is not None:
        sys.stderr.write(answer.stderr)

    sys.exit(answer.return_code)


def dispatch(command_input):
    """
        currently this will handle the given command_input by testing whether it
        fulfills a stub configuration. If so it will save a execution (with the expected flag
        set to true) and send the next answer as defined in the stub configuration object.
    """

    stub_configurations = deserialize_stub_configurations(
        CONFIGURED_STUBS_FILENAME)

    logging.info('Got %s', command_input)

    execution = Execution(
        command_input.command, command_input.arguments, command_input.stdin)

    for stub_configuration in stub_configurations:
        if command_input.fulfills(stub_configuration.command_input):
            logging.info('Execution fulfills %s', stub_configuration)
            execution.mark_as_expected()
            record_execution(execution)
            answer = stub_configuration.next_answer()
            serialize_as_dictionaries(
                CONFIGURED_STUBS_FILENAME, stub_configurations)
            unlock(lock_handle)
            if answer.milliseconds_to_wait:
                time.sleep(answer.milliseconds_to_wait / 1000)
            send_answer(answer)
            return

    unlock(lock_handle)
    logging.error(
        'Given command_input does not fulfill requirements of any stub configuration.')
    sys.exit(255)


def read_stdin():
    """
        waits READ_STDIN_TIMEOUT_IN_SECONDS seconds for input on stdin and
        is going to return the complete input if there is any. If there is no
        input it is going to returns an empty string.
    """
    read_list, _, _ = select(
        [sys.stdin], [], [], READ_STDIN_TIMEOUT_IN_SECONDS)

    if len(read_list) > 0:
        return read_list[0].read()

    return ''


def handle_execution():
    """
        creates the base directory, initializes the logging and will read in
        the arguments and input from stdin to create a new execution object.
    """

    if not os.path.exists(BASEDIR):
        os.mkdir(BASEDIR)
    global lock_handle
    lock_handle = lock(SERIALIZATION_LOCK_FILENAME)

    logging_format = '%(asctime)s %(levelname)5s [%(name)s] process[%(process)d] thread[%(thread)d] - %(message)s'
    logging.basicConfig(filename=LOG_FILENAME,
                        level=logging.INFO,
                        format=logging_format)

    command = os.path.basename(sys.argv[0])
    arguments = sys.argv[1:]
    stdin = read_stdin()

    command_input = CommandInput(command, arguments, stdin)

    dispatch(command_input)


if __name__ == '__main__':  # pragma: no cover
    handle_execution()
