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

class Execution (object):
    def __init__ (self, command, arguments, stdin):
        self.command   = command
        self.arguments = arguments or []
        self.stdin     = stdin
    
    def as_dictionary (self):
        return {'command'   : self.command,
                'arguments' : self.arguments,
                'stdin'     : self.stdin}
    
    def fulfills (self, expectation):
        if self.command != expectation.command:
            return False
        
        if expectation.stdin != self.stdin:
            return False
        
        for argument in expectation.arguments:
            if argument not in self.arguments:
                return False
        
        return True

    def __eq__ (self, other):
        return   self.command == other.command \
           and     self.stdin == other.stdin \
           and self.arguments == other.arguments
    
    def __ne__ (self, other):
        return not(self == other)
    
    def __str__ (self):
        return 'Execution %s' % (self.as_dictionary())
    
    @staticmethod
    def from_dictionary (input_map):
        return Execution(input_map['command'],
                         input_map['arguments'],
                         input_map['stdin'])
