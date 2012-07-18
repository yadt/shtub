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

from shtub.answer import Answer
from shtub.execution import Execution


class Expectation (Execution):
    def __init__ (self, command, arguments, stdin,
                  answers=[], initial_answer=0):
        super(Expectation, self).__init__(command, arguments, stdin)
        
        self.answers        = []
        self.current_answer = initial_answer
        
        for answer in answers:
            self.answers.append(answer)
            
    def as_dictionary (self):
        answers_list = []
        
        for answer in self.answers:
            answer_dictionary = answer.as_dictionary()
            answers_list.append(answer_dictionary)
        
        result = Execution.as_dictionary(self)
        result['answers']        = answers_list
        result['current_answer'] = self.current_answer        
        return result

    def next_answer (self):
        if len(self.answers) == 0:
            raise Exception('No answer given!')
        
        result = self.answers[self.current_answer]
        
        if self.current_answer < len(self.answers) - 1:
            self.current_answer += 1
        
        return result
        
    def then (self, answer):
        self.answers.append(answer)
        
        return self
    
    def then_answer (self, stdout=None, stderr=None, return_code=0):
        return self.then(Answer(stdout, stderr, return_code))
        
    def then_return (self, return_code):
        return self.then_answer(return_code=return_code)

    def then_write (self, stdout=None, stderr=None):
        return self.then_answer(stdout=stdout, stderr=stderr)
    
    def __eq__ (self, other):
        return Execution.__eq__(self, other) \
           and self.current_answer == other.current_answer \
           and self.answers == other.answers

    def __str__ (self):
        return 'Expectation %s' % (self.as_dictionary())
    
    @staticmethod
    def from_dictionary (input_map):
        answers = []
        
        for answer_dictionary in input_map['answers']:
            answer = Answer.from_dictionary(answer_dictionary)
            answers.append(answer)
        
        expectation = Expectation(input_map['command'],
                                  input_map['arguments'],
                                  input_map['stdin'],
                                  answers,
                                  input_map['current_answer'])
        
        return expectation
