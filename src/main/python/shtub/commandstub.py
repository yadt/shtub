#!/usr/bin/env python
#
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

"""
    the command stub.
"""

__author__ = 'Alexander Metzner, Michael Gruber, Udo Juettner'

import logging
import os
import sys
import fcntl

from select import select

from shtub import (BASEDIR,
                   EXECUTIONS_FILENAME,
                   EXPECTATIONS_FILENAME,
                   LOCK_FILENAME,
                   LOG_FILENAME,
                   READ_STDIN_TIMEOUT_IN_SECONDS,
                   deserialize_executions,
                   deserialize_expectations,
                   serialize_executions)

from shtub.execution import Execution
from shtub.commandinput import CommandInput


def lock ():
    """
        creates a file lock and blocks if the file lock is already locked.
    """

    logging.info('Acquire lock.')
    file_handle = open(LOCK_FILENAME, mode='a')
    fcntl.flock(file_handle, fcntl.LOCK_EX)

    logging.info('Lock acquired.')
    return file_handle


def unlock (file_handle):
    """
        releases the given file lock by closing it.
    """

    logging.info('Release lock.')
    file_handle.close()


def record_execution (execution):
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
    serialize_executions(EXECUTIONS_FILENAME, executions)
    logging.info('Recorded %s executions.', len(executions))

    unlock(lock_file_handle)


def send_answer (answer):
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


def dispatch (command_input):
    """
        currently this will handle the given command_input by testing whether it
        fulfills an expectation. If so it will save a execution (with the expected flag
        set to true) and send the next answer as defined in the expectation object.
    """

    expectations = deserialize_expectations(EXPECTATIONS_FILENAME)

    logging.info('Got %s', command_input)

    execution = Execution(command_input.command, command_input.arguments, command_input.stdin)
    
    for expectation in expectations:
        if command_input.fulfills(expectation.command_input):
            logging.info('Execution fulfills %s', expectation)
            
            execution.mark_as_expected()
            record_execution(execution)
            answer = expectation.next_answer()
            send_answer(answer)
            return

    logging.error('Given command_input does not fulfill requirements of any expectation.')
    sys.exit(255)


def read_stdin ():
    """
        waits READ_STDIN_TIMEOUT_IN_SECONDS seconds for input on stdin and
        is going to return the complete input if there is any. If there is no
        input it is going to return None.
    """

    read_list, _, _ = select([sys.stdin], [], [], READ_STDIN_TIMEOUT_IN_SECONDS)

    if len(read_list) > 0:
        return read_list[0].read()

    # quickfix: returning empty string instead of None, to make sure there are no differences
    #           between execution in tty and without.
    return ''


def handle_execution ():
    """
        creates the base directory, initializes the logging and will read in
        the arguments and input from stdin to create a new execution object.
    """

    if not os.path.exists(BASEDIR):
        os.mkdir(BASEDIR)

    logging_format = '%(asctime)s %(levelname)5s [%(name)s] process[%(process)d] thread[%(thread)d] - %(message)s'
    logging.basicConfig(filename=LOG_FILENAME,
                        level=logging.INFO,
                        format=logging_format)

    command   = os.path.basename(sys.argv[0])
    arguments = sys.argv[1:]
    stdin     = read_stdin()
    
    command_input = CommandInput(command, arguments, stdin)

    dispatch(command_input)


if __name__ == '__main__':
    handle_execution()
