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

class Answer (object):
    def __init__(self, stdout, stderr, return_code):
        self.stdout      = stdout
        self.stderr      = stderr
        self.return_code = return_code
        
    def as_dictionary (self):
        return {'stdout'      : self.stdout,
                'stderr'      : self.stderr,
                'return_code' : self.return_code}

    def __str__ (self):
        return 'Answer %s' % (self.as_dictionary())
    
    def __eq__ (self, other):
        return self.stdout == other.stdout \
           and self.stderr == other.stderr \
           and self.return_code == other.return_code

    @staticmethod
    def from_dictionary (input_map):
        return Answer(input_map['stdout'],
                      input_map['stderr'],
                      input_map['return_code'])
