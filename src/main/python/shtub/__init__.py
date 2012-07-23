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
    shtub - shell command stub.
"""

__author__ = 'Alexander Metzner, Michael Gruber, Udo Juettner'

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
    """
        writes the given execution objects into a json file with the given
        filename.
    """
    
    dictionaries = map(lambda e: e.as_dictionary(), executions)
    json_string  = json.dumps(dictionaries, sort_keys=True, indent=4)

    with open(filename, 'w') as json_file:
        json_file.write(json_string)


def load_json_file (filename):
    """
        loads the given json file and returns the json content as dictionary.
    """
    
    with open(filename, 'r') as json_file:
        file_content = json_file.read()
        data = json.loads(file_content)

    return data


def deserialize_stub_executions (filename):
    """
        loads the given json file and returns a list of executions.
    """
    
    executions = load_json_file(filename)
    return map(lambda e: Execution.from_dictionary(e), executions) 


def deserialize_expectations (filename):
    """
        loads the given json file and returns a list of expectations.
    """
    
    expectations = load_json_file(filename)
    return map(lambda e: Expectation.from_dictionary(e), expectations) 
