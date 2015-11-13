# Doodling around with generating functions from ASTs.

import ast

source = """
def ctor(self, a, b, c):
    self._a = a
    self._b = b
    self._c = c
    print(self._c)
"""


class Visitor(ast.NodeVisitor):
    def __init__(self):
        self.level = 0

    def visit(self, node):
        # return super().visit(node)
        indent = '  ' * self.level
        print(indent, node)
        self.level += 1
        try:
            super().visit(node)
        finally:
            self.level -= 1


#tree = ast.parse(source)
#Visitor().visit(tree)


def gen_ctor():
    """This generates a constructor taking a single argument 'a' which it assigned
    to the instance attribute '_a'.

    This is primarily a demo of how to generate a constructor using ASTs. This
    could be expanded to, for example, take a description of the members a
    class should have, creating a custom constructor for it.
    """
    arg_self = ast.arg('self', None)
    arg_a = ast.arg('a', None)
    args = ast.arguments(
        args=[arg_self, arg_a],
        vararg=None,
        kwonlyargs=[],
        kwarg=None,
        defaults=[],
        kw_defaults=[])

    assigner = ast.Assign(
        targets=[
            ast.Attribute(
                value=ast.Name(id='self', ctx=ast.Load()),
                attr='_a',
                ctx=ast.Store())
        ],
        value=ast.Name('a', ast.Load()))

    func = ast.FunctionDef(
        name='ctor',
        args=args,
        body=[assigner],
        decorator_list=[],
        returns=None)

    node = ast.Module(body=[func])
    node = ast.fix_missing_locations(node)
    d = {}
    exec(compile(node, '<ast>', 'exec'), d)
    return d['ctor']


class Shell:
    pass

ctor = gen_ctor()
print(ctor)

setattr(Shell, '__init__', ctor)
s = Shell(42)
print(s._a)

