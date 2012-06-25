import json
import os.path

from shtub.execution import Execution
from shtub.expectation import Expectation


BASEDIR                 = 'test-execution'

EXPECTATIONS_FILENAME   = os.path.join(BASEDIR, 'expectations')
RECORDED_CALLS_FILENAME = os.path.join(BASEDIR, 'recorded-calls')
LOG_FILENAME            = os.path.join(BASEDIR, 'log')
STUBS_DIR               = os.path.join(BASEDIR, 'stubs')


def serialize_stub_executions (filename, executions):
    dictionaries = map(lambda (e): e.as_dictionary(), executions)
    json_string = json.dumps(dictionaries, sort_keys=True, indent=4)

    with open(filename, 'w') as json_file:
        json_file.write(json_string)

def deserialize_stub_executions (filename):
    with open(filename, 'r') as json_file:
        return map(lambda (e): Execution.from_dictionary(e),
                   json.loads(json_file.read())) 

def deserialize_expectations (filename):
    with open(filename, 'r') as json_file:
        return map(lambda (e): Expectation.from_dictionary(e),
                   json.loads(json_file.read())) 
