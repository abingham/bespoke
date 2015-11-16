import unittest

from bespoke.untyped import make_untyped_record


Person = make_untyped_record('name', 'age')


class UntypedRecordTests(unittest.TestCase):
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
