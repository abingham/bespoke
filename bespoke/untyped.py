import ast

class UntypedRecord:
    pass


def _make_ctor(*fields):
    # Define the signature for the constructor
    ctor_args = [ast.arg('self', None)] + [ast.arg(f, None) for f in fields]
    ctor_args = ast.arguments(
        args=ctor_args,
        vararg=None,
        kwonlyargs=[],
        kwarg=None,
        defaults=[],
        kw_defaults=[])

    # Assign the paramters to attributes
    def make_assigner(field):
        return ast.Assign(
            targets=[
                ast.Attribute(
                    value=ast.Name(id='self', ctx=ast.Load()),
                    attr='_' + field,
                    ctx=ast.Store())
            ],
            value=ast.Name(field, ast.Load()))

    assigners = [make_assigner(f) for f in fields]

    func = ast.FunctionDef(
        name='ctor',
        args=ctor_args,
        body=assigners,
        decorator_list=[],
        returns=None)

    node = ast.Module(body=[func])
    node = ast.fix_missing_locations(node)
    d = {}
    exec(compile(node, '<ast>', 'exec'), d)
    return d['ctor']


def _make_property(name):
    args = [ast.arg('self', None)]
    args = ast.arguments(
        args=args,
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

    node = ast.Module(body=[func])
    node = ast.fix_missing_locations(node)
    d = {}
    exec(compile(node, '<ast>', 'exec'), d)
    return d[name]


def make_untyped_record(*fields):
    class Shell:
        pass

    ctor = _make_ctor(*fields)
    setattr(Shell, '__init__', ctor)

    for field in fields:
        setattr(Shell, field, _make_property(field))

    return Shell
