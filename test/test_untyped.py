import unittest

from bespoke.untyped import Field, make_untyped_record

PERSON_DOCSTRING = "Important demographic info for a person."
PERSON_AGE_DOCSTRING = "The person's age"
PERSON_NAME_DOCSTRING = "The person's name"

Person = make_untyped_record(
    Field(name='name',
          docstring=PERSON_NAME_DOCSTRING),
    Field(name='age',
          docstring=PERSON_AGE_DOCSTRING),
    docstring=PERSON_DOCSTRING)


class UntypedRecordTests(unittest.TestCase):
    def test_class_docstring(self):
        self.assertEqual(Person.__doc__, PERSON_DOCSTRING)

    def test_property_docstring(self):
        self.assertEqual(Person.name.__doc__, PERSON_NAME_DOCSTRING)
        self.assertEqual(Person.age.__doc__, PERSON_AGE_DOCSTRING)

    def test_constructor_takes_ordered_arguments(self):
        p = Person('Joe', 42)
        self.assertEqual(p.name, 'Joe')
        self.assertEqual(p.age, 42)

    def test_constructor_takes_keyword_arguments(self):
        p = Person(age=42, name='Joe')
        self.assertEqual(p.name, 'Joe')
        self.assertEqual(p.age, 42)

    def test_property_setting(self):
        p = Person(age=42, name='Joe')
        p.age = 2001
        p.name = 'HAL'

        self.assertEqual(p.name, 'HAL')
        self.assertEqual(p.age, 2001)
