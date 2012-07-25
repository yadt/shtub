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
    This module provides a class called Answer, which represents the answer
    the command stub will send when an expectation is fulfilled.
"""

__author__ = 'Michael Gruber'

class Answer (object):
    """
        represents a answer the command stub is sending back when an expectation
        is fulfilled.
    """
    
    def __init__(self, stdout, stderr, return_code):
        """
            initializes with the given properties.
        """
        
        self.stdout      = stdout
        self.stderr      = stderr
        self.return_code = return_code
    
    
    def as_dictionary (self):
        """
            returns a dictionary representation of this object.
        """
        
        return {'stdout'      : self.stdout,
                'stderr'      : self.stderr,
                'return_code' : self.return_code}


    def __str__ (self):
        """
            returns a string representation of this object using the method
            as_dictionary.
        """
        
        return 'Answer %s' % (self.as_dictionary())


    def __eq__ (self, other):
        """
            returns True when the given answer object has exactly the same
            properties.
        """
        
        return      self.stdout == other.stdout \
           and      self.stderr == other.stderr \
           and self.return_code == other.return_code


    @staticmethod
    def from_dictionary (dictionary):
        """
            returns a new Answer object with the properties from the dictionary.
        """
        
        return Answer(dictionary['stdout'],
                      dictionary['stderr'],
                      dictionary['return_code'])
