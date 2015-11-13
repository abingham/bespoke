import pickle
import unittest

from bespoke.field import field
from bespoke.record_meta import RecordMeta

NAME_DOCSTRING_FIRST_SENTENCE = "The person's name."
NAME_DOCSTRING = """{}

This is a pretty important part of the class.
""".format(NAME_DOCSTRING_FIRST_SENTENCE)

AGE_DOCSTRING_FIRST_SENTENCE = "The person's age."
AGE_DOCSTRING = """{}

It's all mental.
""".format(AGE_DOCSTRING_FIRST_SENTENCE)


class Person(metaclass=RecordMeta):
    name = field(str, default='',
                 documentation=NAME_DOCSTRING)
    age = field(int, default=0,
                documentation=AGE_DOCSTRING)


class RecordConstructionTests(unittest.TestCase):
    def test_smoke_test(self):
        p = Person(name='Douglas',
                   age=42)
        self.assertEqual(p.name, 'Douglas')
        self.assertEqual(p.age, 42)

    def test_constructor_checks_types(self):
        with self.assertRaises(ValueError):
            Person(name='Douglas', age='Forty-Two')

    def test_constructor_checks_keywords(self):
        with self.assertRaises(TypeError):
            Person(name='Douglas', age=42, foo='bar')

    def test_constructor_applies_defaults(self):
        p = Person()
        self.assertEqual(p.name, '')
        self.assertEqual(p.age, 0)


class RecordFieldTests(unittest.TestCase):
    def setUp(self):
        self.p = Person(name='Arthur', age=2001)

    def test_class_has_correct_fields(self):
        self.assertTrue(hasattr(self.p, 'name'))
        self.assertTrue(hasattr(self.p, 'age'))

    def test_class_does_not_have_arbitrary_fields(self):
        self.assertFalse(hasattr(self.p, 'airlock'))
        self.assertFalse(hasattr(self.p, 'monolith'))

    def test_assignment_through_attributes(self):
        self.p.name = "HAL"
        self.p.age = 9000
        self.assertEqual(self.p.name, "HAL")
        self.assertEqual(self.p.age, 9000)

    def test_assignment_checks_types(self):
        with self.assertRaises(ValueError):
            self.p.age = "I'm afraid I can't do that."


class FieldDocstringTests(unittest.TestCase):
    def test_field_docstring(self):
        self.assertEqual(Person.name.__doc__, NAME_DOCSTRING_FIRST_SENTENCE)
        self.assertEqual(Person.age.__doc__, AGE_DOCSTRING_FIRST_SENTENCE)


class RecordPickleTests(unittest.TestCase):
    def test_pickle_and_unpickle(self):
        p = Person(name='Vlassic', age=100)
        pickled = pickle.dumps(p)
        unpickled = pickle.loads(pickled)
        self.assertEqual(p.name, unpickled.name)
        self.assertEqual(p.age, unpickled.age)
