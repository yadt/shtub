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
    this module provides the class Expectation which extends Execution with
    a list of answers and the index of the current answer.
"""

__author__ = 'Alexander Metzner, Michael Gruber, Udo Juettner'

from shtub.answer import Answer
from shtub.commandinput import CommandInput

class Expectation (object):
    """
        Represents the parameters of a expected command stub execution and
        contains corresponding answers.
    """
    
    # quickfix: stdin default is empty string to ensure no difference between execution
    #           in tty and without.
    def __init__ (self, command, arguments=[], stdin='', answers=[], initial_answer=0):
        """
            will initialize a new object with the given properties.
            answers and initial_answer are not mandatory.
        """
        
        self.command_input = CommandInput(command, arguments, stdin)
        
        self.answers        = []
        self.current_answer = initial_answer
        
        for answer in answers:
            self.answers.append(answer)
            
        self.and_input = self.with_input
    
    
    def as_dictionary (self):
        """
            returns a dictionary representation of this expectation.
        """
        
        answers_list = []
        
        for answer in self.answers:
            answer_dictionary = answer.as_dictionary()
            answers_list.append(answer_dictionary)
        
        result = {'command_input'  : self.command_input.as_dictionary(),
                  'answers'        : answers_list,
                  'current_answer' : self.current_answer}
                
        return result


    def next_answer (self):
        """
            returns the next answer in the list of answers or if the end of the
            list is reached it will repeatedly return the last answer of the
            list.
        """
        
        if len(self.answers) == 0:
            raise Exception('List of answers is empty!')
        
        result = self.answers[self.current_answer]
        
        if self.current_answer < len(self.answers) - 1:
            self.current_answer += 1
        
        return result
        
        
    def then (self, answer):
        """
            will append the given answer to the list of answers and return
            the object itself for invocation chaining.
        """
        
        self.answers.append(answer)
        
        return self
    
    
    def then_answer (self, stdout=None, stderr=None, return_code=0):
        """
            a convinience method to "then" which will create a new answer
            object with the given properties. 
        """
        
        return self.then(Answer(stdout, stderr, return_code))
        
        
    def then_return (self, return_code):
        """
            a convinience method to "then" which will create a new answer
            object with the given return_code. 
        """
        
        return self.then_answer(return_code=return_code)


    def then_write (self, stdout=None, stderr=None):
        """
            a convinience method to "then" which will create a new answer
            object with the given stdout and stderr output. 
        """
        
        return self.then_answer(stdout=stdout, stderr=stderr)
    
    
    def with_arguments (self, *arguments):
        """
            sets the given arguments and returns the expectation itself for
            invocation chaining
        """
        
        self.command_input.arguments = list(arguments)
        
        return self

    
    def with_input (self, stdin):
        """
            sets the given arguments and returns the expectation itself for
            invocation chaining
        """
        
        self.command_input.stdin = stdin
        
        return self


    def __eq__ (self, other):
        return  self.command_input == other.command_input \
           and self.current_answer == other.current_answer \
           and        self.answers == other.answers


    def __str__ (self):
        """
            returns a string representation of this expectation using
            as_dictionary
        """
        
        return 'Expectation %s' % (self.as_dictionary())
    
    
    @staticmethod
    def from_dictionary (dictionary):
        """
            returns a new expectation object with the properties from the given
            dictionary.
        """
        
        answers = []
        
        for answer_dictionary in dictionary['answers']:
            answer = Answer.from_dictionary(answer_dictionary)
            answers.append(answer)
        
        command_input_dictionary = dictionary['command_input']
        expectation = Expectation(command_input_dictionary['command'],
                                  command_input_dictionary['arguments'],
                                  command_input_dictionary['stdin'],
                                  answers,
                                  dictionary['current_answer'])
        
        return expectation
