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
    this module provides the class VerifierLoader which offers methods to verify if
    the command stub has been called in the expected way.
"""

__author__ = 'Alexander Metzner, Michael Gruber, Udo Juettner'

import sys
import os.path
from shtub import EXECUTIONS_FILENAME, deserialize_executions
from shtub.verification.commandinputverifier import CommandInputVerifier
from shtub.verification import VerificationException


class Verifier (object):

    def __init__(self, executions):
        self.executions = executions

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        """
            since this class is designed to be integrated in a "with" block it
            is implemented, but has no effect.

            @return: False, when exception_type, exception_value or traceback given,
                     otherwise None
        """

        if exception_type or exception_value or traceback:
            return False

        count_of_executions = len(self.executions)
        if count_of_executions > 0:
            if count_of_executions == 1:
                message = 'There is an unverified execution:\n'
            else:
                message = 'There are %s unverified executions:\n' % count_of_executions

            for execution in self.executions:
                message += "    %s\n" % str(execution)

            raise VerificationException(message)

    def render_execution_chain(self, filelike=sys.stdout):
        filelike.write("%20s\n" % "Execution chain")
        execution_counter = 1
        for e in self.executions:
            ci = e.command_input
            filelike.write("{0} | {1} {2}\n".format(execution_counter, ci.command, ' '.join(ci.arguments)))
            execution_counter += 1

    def called(self, command):
        """
            raises an exception when no more executions are available or
            when the current execution does not have the expected command
            attribute, otherwise it will return the execution and remove the
            current execution from the list of executions.
        """
        if not self.executions:
            raise VerificationException('No more further executions: command "%s" can not be verified.' % command)

        actual_execution = self.executions.pop(0)
        if actual_execution.command_input.command != command:
            raise VerificationException('Execution does not fulfill stub configuration:\n'
                                        'Expected command "%s", but got "%s"\n'
                                        % (command, actual_execution.command_input.command))

        return CommandInputVerifier(actual_execution.command_input)

    def finished(self):
        """
            removes all left executions.
        """
        self.executions = []


class VerifierLoader (Verifier):
    """
        Verifies command stub executions. Please use instances of this class in "with" statements.
    """
    def __init__(self, basedir):
        """
            initializes a new verifier using the given base directory.
        """
        self.base_dir = basedir
        self.executions = []

    def __enter__ (self):
        """
            since this class is designed to be integrated in a "with" block it
            will load the actual executions and return itself.
        """
        filename = os.path.join(self.base_dir, EXECUTIONS_FILENAME)

        if not os.path.exists(filename):
            raise VerificationException('No executions found. Stubbed commands have never been called.')

        self.executions = deserialize_executions(filename)

        for execution in self.executions:
            if not execution.expected:
                raise VerificationException('Unexpected %s: did not fulfill any stub configuration.' % str(execution))

        return self

    def filter_by_argument(self, argument_name):
        matching_executions = []

        for execution in self.executions:
            for current_argument in execution.command_input.arguments:
                if current_argument.startswith(argument_name):
                    matching_executions.append(execution)

        return Verifier(matching_executions)
