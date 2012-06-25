import unittest

from shtub.execution import Execution

class ExecutionTests (unittest.TestCase):
    def test_should_convert_dictionary_to_object (self):
        values = dict (
            command= 'any_command',
            arguments= ['any_arguments'],
            stdin= 'any_stdin'
        )
        
        actual_execution = Execution.from_dictionary(values)
        
        self.assertEquals('any_command', actual_execution.command)
        self.assertEquals(['any_arguments'], actual_execution.arguments)
        self.assertEquals('any_stdin', actual_execution.stdin)

    def test_should_create_object_with_given_properties (self):
        actual_execution = Execution('any_command', ['any_arg1', 'any_arg2'], 'any_stdin')
        
        self.assertEquals('any_command', actual_execution.command)
        self.assertEquals(['any_arg1', 'any_arg2'], actual_execution.arguments)
        self.assertEquals('any_stdin', actual_execution.stdin)

    def test_should_create_object_with_given_properties_but_empty_arguments (self):
        actual_execution = Execution('any_command', [], 'any_stdin')
        
        self.assertEquals('any_command', actual_execution.command)
        self.assertEquals([], actual_execution.arguments)
        self.assertEquals('any_stdin', actual_execution.stdin)
        
    def test_should_convert_object_to_dictionary (self):
        execution = Execution('any_command', ['any_arg1', 'any_arg2'], 'any_stdin')

        actual_dictionary = execution.as_dictionary()
        
        self.assertEquals('any_command', actual_dictionary['command'])
        self.assertEquals(['any_arg1', 'any_arg2'], actual_dictionary['arguments'])
        self.assertEquals('any_stdin', actual_dictionary['stdin'])
    
    def test_should_return_false_when_objects_command_is_not_equal (self):
        execution1 = Execution('any_command', ['any_arg1', 'any_arg2'], 'any_stdin')
        execution2 = Execution('other_command', ['any_arg1', 'any_arg2'], 'any_stdin')
        
        self.assertFalse(execution1 == execution2, 'comparison of command')

    def test_should_return_false_when_objects_stdin_is_not_equal (self):
        execution1 = Execution('any_command', ['any_arg1', 'any_arg2'], 'any_stdin')
        execution2 = Execution('any_command', ['any_arg1', 'any_arg2'], 'other_stdin')

        self.assertFalse(execution1 == execution2, 'comparison of stdin')

    def test_should_return_false_when_objects_arguments_are_not_equal (self):
        execution1 = Execution('any_command', ['any_arg1', 'any_arg2'], 'any_stdin')
        execution2 = Execution('any_command', ['other_argument1', 'any_arg2'], 'any_stdin')
    
        self.assertFalse(execution1 == execution2, 'comparison of arguments')

    def test_should_return_true_when_objects_are_equal (self):
        execution1 = Execution('any_command', ['any_arg1', 'any_arg2'], 'any_stdin')
        execution2 = Execution('any_command', ['any_arg1', 'any_arg2'], 'any_stdin')
        
        self.assertTrue(execution1 == execution2, 'no difference, but not equal returned')

    def test_should_return_false_when_objects_are_equal_and_testing_if_not_equal (self):
        execution1 = Execution('any_command', ['any_arg1', 'any_arg2'], 'any_stdin')
        execution2 = Execution('any_command', ['any_arg1', 'any_arg2'], 'any_stdin')
        
        self.assertFalse(execution1 != execution2, 'no difference, but not equal returned')
        
    def test_should_return_true_when_objects_are_not_equal_and_testing_if_not_equal (self):
        execution1 = Execution('any_command', ['any_arg1', 'any_arg2'], 'any_stdin')
        execution2 = Execution('other_command', ['other_argument1', 'other_argument2'], 'other_stdin')
        
        self.assertTrue( execution1 != execution2, 'comparison: stdin')

    def test_should_return_string_with_all_properties (self):
        execution = Execution('any_command', ['any_arg1', 'any_arg2'], 'any_stdin')
        
        self.assertEquals("Execution {'stdin': 'any_stdin', 'command': 'any_command', 'arguments': ['any_arg1', 'any_arg2']}", str(execution))

    def test_should_return_false_if_other_has_different_arguments (self):
        execution = Execution('any_command', ['any_arg1', 'any_arg2'], 'any_stdin')
        other_execution = Execution('any_command', ['other_argument1', 'other_argument2'], 'any_stdin')

        self.assertFalse(execution.fulfills(other_execution))

    def test_should_return_false_if_other_has_at_least_one_different_argument (self):
        execution = Execution('any_command', ['any_arg1', 'any_arg2'], 'any_stdin')
        other_execution = Execution('any_command', ['any_arg1', 'any_arg2', 'other_argument'], 'any_stdin')

        self.assertFalse(execution.fulfills(other_execution))

    def test_should_return_true_if_other_has_no_arguments (self):
        execution = Execution('any_command', ['any_arg1', 'any_arg2'], 'any_stdin')
        other_execution = Execution('any_command', [], 'any_stdin')

        self.assertTrue(execution.fulfills(other_execution))

    def test_should_return_true_if_other_has_exactly_one_matching_argument_and_no_others (self):
        execution = Execution('any_command', ['any_arg1', 'any_arg2'], 'any_stdin')
        other_execution = Execution('any_command', ['any_arg1'], 'any_stdin')

        self.assertTrue(execution.fulfills(other_execution))

    def test_should_return_true_if_other_has_equal_arguments (self):
        execution = Execution('any_command', ['any_arg1', 'any_arg2'], 'any_stdin')
        other_execution = Execution('any_command', ['any_arg2', 'any_arg1'], 'any_stdin')

        self.assertTrue(execution.fulfills(other_execution))

    def test_should_return_false_when_other_has_different_command_but_equal_arguments (self):
        execution = Execution('any_command', ['any_arg1', 'any_arg2'], 'any_stdin')
        other_execution = Execution('other_command', ['any_arg2', 'any_arg1'], 'any_stdin')

        self.assertFalse(execution.fulfills(other_execution), 'comparison: command')

    def test_should_return_false_when_other_has_different_stdin (self):
        execution = Execution('any_command', ['any_arg1', 'any_arg2'], 'any_stdin')
        other_execution = Execution('any_command', ['any_arg1', 'any_arg2'], 'other_stdin')

        self.assertFalse(execution.fulfills(other_execution), 'comparison: stdin')

    def test_should_return_true_when_other_equal_command_and_arguments (self):
        execution = Execution('any_command', ['any_arg1', 'any_arg2'], 'any_stdin')
        other_execution = Execution('any_command', ['any_arg2', 'any_arg1'], 'any_stdin')

        self.assertTrue(execution.fulfills(other_execution), 'comparison: command')
