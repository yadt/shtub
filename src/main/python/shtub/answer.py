class Answer (object):
    def __init__(self, stdout, stderr, return_code):
        self.stdout = stdout
        self.stderr = stderr
        self.return_code = return_code
        
    def as_dictionary (self):
        return dict(
            stdout = self.stdout,
            stderr = self.stderr,
            return_code = self.return_code
        )

    def __str__ (self):
        return 'Answer %s' % (self.as_dictionary())
    
    def __eq__ (self, other):
        return self.stdout == other.stdout \
            and self.stderr == other.stderr \
            and self.return_code == other.return_code

    @staticmethod
    def from_dictionary (input_map):
        return Answer(input_map['stdout'], input_map['stderr'], input_map['return_code'])
