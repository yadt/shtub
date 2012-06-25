import unittest

from shtub.answer import Answer


class AnswerTest (unittest.TestCase):
    def test_should_create_new_instance_with_given_values (self):
        actual_answer = Answer('Hello world!', 'Hello error!', 8)
        
        self.assertEquals('Hello world!', actual_answer.stdout)
        self.assertEquals('Hello error!', actual_answer.stderr)
        self.assertEquals(8, actual_answer.return_code)

    def test_should_return_answer_from_dictionary (self):
        answer_dictionary = dict(
            stdout = 'Hello world.',
            stderr = 'Hello error!',
            return_code = 82
        )
        
        actual_answer = Answer.from_dictionary(answer_dictionary)
        
        self.assertEquals('Hello world.', actual_answer.stdout)
        self.assertEquals('Hello error!', actual_answer.stderr)
        self.assertEquals(82, actual_answer.return_code)

    def test_should_return_answer_as_dictionary (self):
        answer = Answer('Hello world.', 'Hello error!', 13)
        
        actual_dictionary = answer.as_dictionary()
        
        self.assertEquals('Hello world.', actual_dictionary['stdout'])
        self.assertEquals('Hello error!', actual_dictionary['stderr'])
        self.assertEquals(13, actual_dictionary['return_code'])
    
    def test_should_return_answer_as_string (self):
        answer = Answer('Hello world.', 'Hello error!', 13)
        
        actual_string = answer.__str__()
        
        self.assertEquals("Answer {'return_code': 13, 'stderr': 'Hello error!', 'stdout': 'Hello world.'}", actual_string)
        
    def test_should_return_false_when_comparing_and_stdout_is_different (self):
        answer1 = Answer('Hello world.', 'Hello error!', 13)
        answer2 = Answer('Spam eggs', 'Hello error!', 13)
        
        self.assertFalse(answer1 == answer2, 'comparison error: attribute stdout')
        
    def test_should_return_false_when_comparing_and_stdout_is_different (self):
        answer1 = Answer('Hello world.', 'Hello error!', 13)
        answer2 = Answer('Hello world.', 'Spam eggs', 13)
        
        self.assertFalse(answer1 == answer2, 'comparison error: attribute stderr')
        
    def test_should_return_false_when_comparing_and_return_code_is_different (self):
        answer1 = Answer('Hello world.', 'Hello error!', 13)
        answer2 = Answer('Hello world.', 'Hello error!', 0)
        
        self.assertFalse(answer1 == answer2, 'comparison error: attribute return_code')
        
    def test_should_return_true_when_comparing_and_objects_are_equal (self):
        answer1 = Answer('Hello world.', 'Hello error!', 0)
        answer2 = Answer('Hello world.', 'Hello error!', 0)
        
        self.assertTrue(answer1 == answer2, 'comparison error: objects are equal')
        