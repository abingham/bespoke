# Bespoke: simple Python class factory

Bespoke provides a means to generate classes given a description of the
attributes it should have. It's a bit like `collections.namedtuple` with super
powers.

## Quickstart

In a nutshell
´´´
from bespoke.field import field
from bespoke.record_meta import RecordMeta

class Person(metaclass=RecordMeta):
    name = field(str, default='',
                 documentation="The person's name.")
    age = field(int, default=0,
                documentation="The person's age.")

p = Person(name='Tom', age='13')
assert p.name == 'Tom'
assert p.age == 13

p.name = 'Thomas'
assert p.name == 'Thomas'
´´´
