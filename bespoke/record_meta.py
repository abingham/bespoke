from collections import OrderedDict
from itertools import chain

from .field import NamedField, RecordFieldDescriptor
from .record import Record


class RecordMeta(type):
    """A metaclass for header format classes.
    """

    @classmethod
    def __prepare__(mcs, name, bases, *args, **kwargs):
        return OrderedDict()

    def __new__(mcs, name, bases, namespace):

        # TODO: This is a good point to validate that the fields are in order and that the
        # TODO: format specification is valid.  We shouldn't even build the class otherwise.

        # TODO: Also validate existence of LENGTH_IN_BYTES

        namespace['_ordered_field_names'] = tuple(name for name, attr in namespace.items()
                                                  if isinstance(attr, RecordFieldDescriptor))

        transitive_bases = set(chain.from_iterable(type(base).mro(base) for base in bases))

        if Record not in transitive_bases:
            bases = (Record,) + bases

        for attr_name, attr in namespace.items():

            # This shenanigans is necessary so we can have all the following work is a useful way
            # help(class), help(instance), help(class.property) and help(instance.property)

            # Set the _name attribute of the field instance if it hasn't already been set
            if isinstance(attr, RecordFieldDescriptor):
                if attr._name is None:
                    attr._name = attr_name

            # We rename the *class* and set its docstring so help() works usefully
            # when called with a class containing such fields.
            attr_class = attr.__class__
            if issubclass(attr_class, NamedField) and attr_class is not NamedField:
                attr_class.__name__ = underscores_to_camelcase(attr_name)
                attr_class.__doc__ = attr.documentation

        return super().__new__(mcs, name, bases, namespace)
