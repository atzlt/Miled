from interpreter.interpret import Caller, Env

def product(x):
    p = 1
    for a in x:
        p *= a
    return p


def sort(x):
    x = list(x)
    x.sort()
    return x


BUILTINS_TABLE = Env(table={
    "<-": Caller(2, lambda x, _: (None, [(0, x[1], False)], None)),
    ":=": Caller(2, lambda x, _: (None, [(0, x[1], True)], None)),
    "~": Caller(-1, lambda x, _: (x[-1], [], None)),
    "??": None,

    ">": Caller(2, lambda x, _: (x[0] > x[1], [], None)),
    "<": Caller(2, lambda x, _: (x[0] < x[1], [], None)),
    ">=": Caller(2, lambda x, _: (x[0] >= x[1], [], None)),
    "<=": Caller(2, lambda x, _: (x[0] >= x[1], [], None)),
    "!=": Caller(2, lambda x, _: (x[0] != x[1], [], None)),

    "&": Caller(2, lambda x, _: (x[0] and x[1], [], None)),
    "==": Caller(2, lambda x, _: (x[0] == x[1], [], None)),

    "+": Caller(2, lambda x, _: (x[0] + x[1], [], None)),
    "+=": Caller(2, lambda x, _: (None, [(0, x[0] + x[1], False)], None)),
    "n+": Caller(-1, lambda x, _: (sum(x), [], None)),
    "*": Caller(2, lambda x, _: (x[0] * x[1], [], None)),
    "*=": Caller(2, lambda x, _: (None, [(0, x[0] * x[1], False)], None)),
    "n*": Caller(-1, lambda x, _: (product(x), [], None)),
    "-": Caller(2, lambda x, _: (x[0] - x[1], [], None)),
    "-=": Caller(2, lambda x, _: (None, [(0, x[0] - x[1], False)], None)),
    "/": Caller(2, lambda x, _: (x[0] / x[1], [], None)),
    "/=": Caller(2, lambda x, _: (None, [(0, x[0] / x[1], False)], None)),
    "%": Caller(2, lambda x, _: (x[0] % x[1], [], None)),
    "%=": Caller(2, lambda x, _: (None, [(0, x[0] % x[1], False)], None)),

    "if:": Caller(1, lambda x, _: (None, [], None if x[0] else 0)),
    "if::": Caller(1, lambda x, _: (None, [], None if x[0] else 0)),
    "else": Caller(0, lambda x, _: (None, [], 0)),
    "while:": Caller(1, lambda x, _: (None, [], None if x[0] else 0)),
    ":ihw": Caller(0, lambda x, _: (None, [], 0)),

    "->str": Caller(1, lambda x, _: (str(x[0]), [], None)),
    "->int": Caller(1, lambda x, _: (int(x[0]), [], None)),
    "->dec": Caller(1, lambda x, _: (float(x[0]), [], None)),
    "->lst": Caller(1, lambda x, _: (list(x[0]), [], None)),

    "[": Caller(-1, lambda x, _: (x, [], None)),
    "_:": Caller(2, lambda x, _: (x[0][x[1]], [], None)),
    ":<-": Caller(2, lambda x, _: (None, [(0, x[0][:x[1]] + x[2] + x[0][x[1] + 1:], False)], None)),

    "rev": Caller(1, lambda x, _: (x[::-1], [], None)),
    "divs": Caller(2, lambda x, _: (x[1] % x[0] == 0, [], None)),
    "sort": Caller(1, lambda x, _: (sort(x[0]), [], None)),
})
