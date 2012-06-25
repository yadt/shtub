class Execution (object):
    def __init__ (self, command, arguments, stdin):
        self.command = command
        self.arguments = arguments or []
        self.stdin = stdin
    
    def as_dictionary (self):
        return dict(
            command = self.command,
            arguments = self.arguments,
            stdin = self.stdin
        )
    
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
        return self.command == other.command \
            and self.stdin == other.stdin \
            and self.arguments == other.arguments
    
    def __ne__ (self, other):
        return not(self == other)
    
    def __str__ (self):
        return 'Execution %s' % (self.as_dictionary())
    
    @staticmethod
    def from_dictionary (input_map):
        return Execution(input_map['command'], input_map['arguments'], input_map['stdin'])
