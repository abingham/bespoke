from .util import super_class


class Record:
    """An abstract base class for generated classes."""

    def __init__(self, *args, **kwargs):
        """Initialise a header instance.

        Args:
            *args: Positional arguments are matched with header fields in the order they
                are declared in the class definition (i.e. the same order defined by
                the ordered_field_names() method.  From a performance perspective
                positional arguments are faster than keyword arguments.

            **kwargs: Keyword arguments are assigned to the header field of the same name.
                Keyword argument values will overwrite any positional argument values.

        Raises:
            TypeError: If keyword argument names do not correspond to header fields.
        """
        for keyword, arg in zip(self.ordered_field_names(), args):
            setattr(self, keyword, arg)

        for keyword, arg in kwargs.items():
            try:
                getattr(self, keyword)
            except AttributeError as e:
                raise TypeError("{!r} is not a recognised field name for {!r}"
                                .format(keyword, self.__class__.__name__)) from e
            else:
                setattr(self, keyword, arg)

    _ordered_field_names = tuple()

    @classmethod
    def ordered_field_names(cls):
        """The ordered list of field names.

        This is a metamethod which should be called on cls.

        Returns:
            An tuple containing the field names in order.
        """

        if cls is Record:
            return cls._ordered_field_names
        return super_class(cls).ordered_field_names() + cls._ordered_field_names

    def __getattr__(self, name):
        raise AttributeError("Object of type {!r} has no attribute {!r}".format(self.__class__.__name__, name))

    def __repr__(self):
        return "{}({})".format(
            self.__class__.__name__,
            ', '.join("{}={}".format(k, getattr(self, k)) for k in self.ordered_field_names()))

    def __getstate__(self):
        state = self.__dict__.copy()
        state['__version__'] = __version__
        state['_all_attributes'] = OrderedDict((name, getattr(self, name)) for name in self._ordered_field_names)
        return state

    def __setstate__(self, state):
        if state['__version__'] != __version__:
            raise TypeError("Cannot unpickle {} version {} into version {}"
                            .format(self.__class__.__name__,
                                    state['__version__'],
                                    __version__))
        del state['__version__']

        for name, value in state['_all_attributes'].items():
            setattr(self, name, value)
        del state['_all_attributes']
        self.__dict__.update(state)
