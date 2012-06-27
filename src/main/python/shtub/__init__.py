import json

from os.path import join

from shtub.execution import Execution
from shtub.expectation import Expectation


BASEDIR                         = 'test-execution'

EXPECTATIONS_FILENAME           = join(BASEDIR, 'expectations')
RECORDED_CALLS_FILENAME         = join(BASEDIR, 'recorded-calls')
LOG_FILENAME                    = join(BASEDIR, 'log')
STUBS_DIRECTORY                 = join(BASEDIR, 'stubs')

READ_STDIN_TIMEOUT_IN_SECONDS   = 1


def serialize_stub_executions (filename, executions):
    dictionaries = map(lambda e: e.as_dictionary(), executions)
    json_string  = json.dumps(dictionaries, sort_keys=True, indent=4)

    with open(filename, 'w') as json_file:
        json_file.write(json_string)


def load_json_file (filename):
    with open(filename, 'r') as json_file:
        file_content = json_file.read()
        data = json.loads(file_content)

    return data

def deserialize_stub_executions (filename):
    executions = load_json_file(filename)
    return map(lambda e: Execution.from_dictionary(e), executions) 

def deserialize_expectations (filename):
    expectations = load_json_file(filename)
    return map(lambda e: Expectation.from_dictionary(e), expectations) 
