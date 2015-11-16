import ast
from itertools import chain


def _make_args(*fields):
    return [ast.arg(f, None) for f in fields]


def _make_assigner(attr, value):
    return ast.Assign(
        targets=[
            ast.Attribute(
                value=ast.Name(id='self', ctx=ast.Load()),
                attr=attr,
                ctx=ast.Store())
        ],
        value=ast.Name(value, ast.Load()))


def _make_ctor(*fields, name='__init__'):
    # Define the signature for the constructor
    ctor_args = ast.arguments(
        args=_make_args('self', *fields),
        vararg=None,
        kwonlyargs=[],
        kwarg=None,
        defaults=[],
        kw_defaults=[])

    # Assign the paramters to attributes
    assigners = [_make_assigner('_' + f, f) for f in fields]

    func = ast.FunctionDef(
        name=name,
        args=ctor_args,
        body=assigners,
        decorator_list=[],
        returns=None)

    return func


def _make_property_getter(name):
    args = ast.arguments(
        args=_make_args('self'),
        vararg=None,
        kwonlyargs=[],
        kwarg=None,
        defaults=[],
        kw_defaults=[])

    body = [
        ast.Return(
            ast.Attribute(
                value=ast.Name(id='self', ctx=ast.Load()),
                attr='_' + name,
                ctx=ast.Load()))
    ]

    decorators = [ast.Name(id='property', ctx=ast.Load())]

    func = ast.FunctionDef(
        name=name,
        args=args,
        body=body,
        decorator_list=decorators,
        returns=None)

    return func


def _make_property_setter(name):
    args = ast.arguments(
        args=_make_args('self', 'value'),
        vararg=None,
        kwonlyargs=[],
        kwarg=None,
        defaults=[],
        kw_defaults=[])

    body = [_make_assigner('_' + name, 'value')]

    decorators = [
        ast.Attribute(
            value=ast.Name(id=name, ctx=ast.Load()),
            attr='setter',
            ctx=ast.Load())]

    func = ast.FunctionDef(
        name=name,
        args=args,
        body=body,
        decorator_list=decorators,
        returns=None)

    return func


def make_untyped_record(*fields):
    class Shell:
        pass

    body = chain([_make_ctor(*fields)],
                 [_make_property_getter(f) for f in fields],
                 [_make_property_setter(f) for f in fields])

    mod = ast.Module(body=list(body))
    mod = ast.fix_missing_locations(mod)
    namespace = {}
    exec(compile(mod, '<ast>', 'exec'), namespace)

    for name in chain(['__init__'], fields):
        setattr(Shell, name, namespace[name])

    return Shell
