#!/usr/bin/env python

import logging
import os
import sys

from select import select

from shtub import RECORDED_CALLS_FILENAME, EXPECTATIONS_FILENAME, LOG_FILENAME, BASEDIR, \
            deserialize_expectations, deserialize_stub_executions, serialize_stub_executions
from shtub.execution import Execution
        

def record_call (execution):
    recorded_calls = []
    
    if os.path.exists(RECORDED_CALLS_FILENAME):
        recorded_calls = deserialize_stub_executions(RECORDED_CALLS_FILENAME)
    
    recorded_calls.append(execution)
    
    serialize_stub_executions(RECORDED_CALLS_FILENAME, recorded_calls)
    
    logging.info('Recorded %s calls' % len(recorded_calls))
 
def send_answer (answer):
    logging.info('Sending answer: %s' % answer)
    
    if answer.stdout is not None:
        sys.stdout.write(answer.stdout)

    if answer.stderr is not None:
        sys.stderr.write(answer.stderr)
    
    sys.exit(answer.return_code)
    
def dispatch (execution):
    expectations = deserialize_expectations(EXPECTATIONS_FILENAME)
    
    logging.info('Got execution: %s', execution)

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
    read_list, _, _ = select([sys.stdin], [], [], 1)
    
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
