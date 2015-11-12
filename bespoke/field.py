from weakref import WeakKeyDictionary

from .docstring import docstring_property


class RecordFieldDescriptor:

    def __init__(self, value_type, default, documentation):
        self._named_field = NamedField(value_type, default, documentation)
        self._instance_data = WeakKeyDictionary()

    @property
    def _name(self):
        return self._named_field.name

    @_name.setter
    def _name(self, value):
        self._named_field._name = value

    def __get__(self, instance, owner):
        """Retrieve the format or instance data.

        When called on the class we return a NamedField instance containing the format data. For example:

            line_seq_num_default = TraceHeaderRev1.line_sequence_num.default
            line_seq_num_offset = TraceHeaderRev1.line_sequence_num.offset

        When called on an instance we return the field value.

            line_seq_num = my_trace_header.line_sequence_num
        """
        if instance is None:
            return self._named_field
        if instance not in self._instance_data:
            return self._named_field.default
        return self._instance_data[instance]

    def __set__(self, instance, value):
        """Set the field value."""
        try:
            self._instance_data[instance] = self._named_field._value_type(value)
        except ValueError as e:
            raise ValueError("Assigned value {!r} for {} attribute must be convertible to {}: {}"
                             .format(value, self._name, self._named_field._value_type.__name__, e)) from e

    def __delete__(self, instance):
        raise AttributeError("Can't delete {} attribute".format(self._name))

    @docstring_property(__doc__)
    def __doc__(self):
        return self._named_field._documentation

    # TODO: Get documentation of these descriptors working correctly


class NamedField:
    """Instances of NamedField can be detected by the NamedDescriptorResolver metaclass."""

    def __init__(self, value_type, default, documentation):
        self._name = None  # Set later by the metaclass
        self._value_type = value_type
        self._default = self._value_type(default)
        self._documentation = str(documentation)

    @property
    def name(self):
        "The field name."
        return self._name

    @property
    def value_type(self):
        "The field value type (e.g. Int32)"
        return self._value_type

    @property
    def default(self):
        "The default value of the field. Must be convertible to value_type."
        return self._default

    @property
    def documentation(self):
        "A descriptive text string."
        return self._documentation

    @docstring_property(__doc__)
    def __doc__(self):
        return first_sentence(self._documentation)

    def __repr__(self):
        return "{}(name={!r}, value_type={!r}, offset={!r}, default={!r})".format(
            self.__class__.__name__,
            self.name,
            self.value_type.__name__,
            self.offset,
            self.default)


def field(value_type, default, documentation):
    """
    Args:
        value_type: The type of the field (e.g. Int32)

        default: The default value for this field.

        documentation: A docstring for the field. The first sentence should be usable
            as a brief description.

    Returns:
        An instance of a subclass of NamedField class.
    """

    # Create a class specifically for this field. This class will later get
    # renamed when the NamedDescriptorMangler metaclass does its job, to
    # a class name based on the field name.

    class SpecificField(RecordFieldDescriptor):
        pass

    return SpecificField(value_type, default, documentation)
