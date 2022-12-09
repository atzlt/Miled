from interpreter.interpret import Caller, Env

BUILTIN_CALLERS = {
    "let": Caller(2, lambda x, _: (None, [(0, True, x[1])], None)),
    "set": Caller(2, lambda x, _: (None, [(0, False, x[1])], None)),

    "~": Caller(-1, lambda x, _: (x[-1], [], None)),

    ">": Caller(2, lambda x, _: (x[0] > x[1], [], None)),
    "!=": Caller(2, lambda x, _: (x[0] != x[1], [], None)),

    "+": Caller(2, lambda x, _: (x[0] + x[1], [], None)),
    "+=": Caller(2, lambda x, _: (None, [(0, False, x[0] + x[1])], None)),
    "n+": Caller(-1, lambda x, _: (sum(x), [], None)),
    "-": Caller(2, lambda x, _: (x[0] - x[1], [], None)),
    "-=": Caller(2, lambda x, _: (None, [(0, False, x[0] - x[1])], None)),

    "if:": Caller(1, lambda x, _: (None, [], None if x[0] else 0)),
    "if::": Caller(1, lambda x, _: (None, [], None if x[0] else 0)),
    "else": Caller(0, lambda x, _: (None, [], 0)),
    "while:": Caller(1, lambda x, _: (None, [], None if x[0] else 0)),
    ":ihw": Caller(0, lambda x, _: (None, [], 0)),
}

BUILTINS_TABLE = Env(table=BUILTIN_CALLERS)
