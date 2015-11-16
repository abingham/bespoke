import ast
from itertools import chain


def _make_args(*fields):
    return [ast.arg(f, None) for f in fields]


def _make_assigner(field):
    return ast.Assign(
        targets=[
            ast.Attribute(
                value=ast.Name(id='self', ctx=ast.Load()),
                attr='_' + field,
                ctx=ast.Store())
        ],
        value=ast.Name(field, ast.Load()))


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
    assigners = [_make_assigner(f) for f in fields]

    func = ast.FunctionDef(
        name=name,
        args=ctor_args,
        body=assigners,
        decorator_list=[],
        returns=None)

    return func


def _make_property(name):
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


def make_untyped_record(*fields):
    class Shell:
        pass

    body = [_make_ctor(*fields)] + [_make_property(f) for f in fields]

    mod = ast.Module(body=body)
    mod = ast.fix_missing_locations(mod)
    namespace = {}
    exec(compile(mod, '<ast>', 'exec'), namespace)

    for name in chain(['__init__'], fields):
        setattr(Shell, name, namespace[name])

    return Shell
