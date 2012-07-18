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
    
import logging
import os
import sys
import fcntl

from select import select

from shtub import (BASEDIR,
                   EXPECTATIONS_FILENAME,
                   LOG_FILENAME,
                   RECORDED_CALLS_FILENAME,
                   READ_STDIN_TIMEOUT_IN_SECONDS,
                   deserialize_expectations,
                   deserialize_stub_executions,
                   serialize_stub_executions)

from shtub.execution import Execution
        

def lock ():
    logging.info('Locking process %s' % os.getpid())
    file_handle = open(os.path.join(BASEDIR, 'LOCK'), 'a')
    fcntl.flock(file_handle, fcntl.LOCK_EX)
    logging.info('Lock acquired by process %s' % os.getpid())
    
    return file_handle

def unlock (file_handle):
    logging.info('Unlocking %s' % os.getpid())
    file_handle.close()

def record_call (execution):
    file_handle = lock()
    recorded_calls = []
    
    if os.path.exists(RECORDED_CALLS_FILENAME):
        recorded_calls = deserialize_stub_executions(RECORDED_CALLS_FILENAME)
    
    recorded_calls.append(execution)
    
    serialize_stub_executions(RECORDED_CALLS_FILENAME, recorded_calls)
    
    logging.info('Recorded %s calls' % len(recorded_calls))
    
    unlock(file_handle)
 
def send_answer (answer):
    logging.info('Sending answer: %s' % answer)
    
    if answer.stdout is not None:
        sys.stdout.write(answer.stdout)

    if answer.stderr is not None:
        sys.stderr.write(answer.stderr)
    
    sys.exit(answer.return_code)
    
def dispatch (execution):
    expectations = deserialize_expectations(EXPECTATIONS_FILENAME)
    
    logging.info('Got execution: %s in process %s' % (execution, os.getpid()))

    for expectation in expectations:
        if execution.fulfills(expectation):
            logging.info('Execution fulfills %s', expectation)
            
            record_call(execution)
            answer = expectation.next_answer()
            send_answer(answer)
            return

    logging.error('Execution does not fulfill requirements by any given expectation.')
    sys.exit(255)
 
def read_stdin ():
    read_list, _, _ = select([sys.stdin], [], [], READ_STDIN_TIMEOUT_IN_SECONDS)
    
    if len(read_list) > 0:
        return read_list[0].read()
    
    return None
    
def handle_stub_call ():
    if not os.path.exists(BASEDIR):
        os.mkdir(BASEDIR)

    logging.basicConfig(filename = LOG_FILENAME,
                        level    = logging.INFO,
                        format   = '%(asctime)s %(levelname)5s [%(name)s] - %(message)s')

    command   = os.path.basename(sys.argv[0])
    arguments = sys.argv[1:]
    stdin     = read_stdin()
    execution = Execution(command, arguments, stdin)
    
    dispatch(execution)
    
if __name__ == '__main__':
    handle_stub_call()
