import random
from copy import deepcopy as copy
from interpreter.util_classes import Caller, Env, Token


def product(x):
    p = 1
    for a in x:
        p *= a
    return p


def sort(x):
    x = list(x)
    x.sort()
    return x


def def_new_caller(param_list: list[any], code: list[Token]):
    call_id = str(random.randint(0, 65535))
    suffix = "$call_arg$" + call_id
    for i in range(len(code)):
        if code[i].kind == Token.ID and code[i].value in param_list:
            code[i].value += suffix

    def run_new_caller(param: list, old_table: Env):
        from interpreter.interpret import Interpreter
        table = Env()
        table.prev = old_table
        for j in range(len(param_list)):
            table.force_def(param_list[j] + suffix, param[j])
        ret = Interpreter(code, table, None).run()
        return ret, [], None

    return Caller(
        len(param_list),
        run_new_caller
    )


def map_over(f: Caller, old_list: list, table: Env):
    return [
        copy(f).add_args([i]).enclose().resolve(table)[0]
        for i in old_list
    ]


BUILTINS_TABLE = Env(table={
    "<-": Caller(2, lambda x, _: (None, [(0, x[1], False)], None)),
    ":=": Caller(2, lambda x, _: (None, [(0, x[1], True)], None)),
    "~": Caller(-1, lambda x, _: (x[-1], [], None)),

    "def": Caller(3, lambda x, _: (None, [(0, def_new_caller(x[1], x[2]), True)], None)),

    ">": Caller(2, lambda x, _: (x[0] > x[1], [], None)),
    "<": Caller(2, lambda x, _: (x[0] < x[1], [], None)),
    ">=": Caller(2, lambda x, _: (x[0] >= x[1], [], None)),
    "<=": Caller(2, lambda x, _: (x[0] >= x[1], [], None)),
    "!=": Caller(2, lambda x, _: (x[0] != x[1], [], None)),
    "!": Caller(1, lambda x, _: (not x[0], [], None)),
    "=!": Caller(1, lambda x, _: (None, [(0, not x[0], False)], None)),
    "&": Caller(2, lambda x, _: (x[0] and x[1], [], None)),
    "&=": Caller(2, lambda x, _: (None, [(0, x[0] and x[1], False)], None)),
    "|": Caller(2, lambda x, _: (x[0] or x[1], [], None)),
    "|=": Caller(2, lambda x, _: (None, [(0, x[0] or x[1], False)], None)),
    "==": Caller(2, lambda x, _: (x[0] == x[1], [], None)),

    "+": Caller(2, lambda x, _: (x[0] + x[1], [], None)),
    "+=": Caller(2, lambda x, _: (None, [(0, x[0] + x[1], False)], None)),
    "n+": Caller(-1, lambda x, _: (sum(x), [], None)),
    "*": Caller(2, lambda x, _: (x[0] * x[1], [], None)),
    "*=": Caller(2, lambda x, _: (None, [(0, x[0] * x[1], False)], None)),
    "n*": Caller(-1, lambda x, _: (product(x), [], None)),
    "-": Caller(2, lambda x, _: (x[0] - x[1], [], None)),
    "--": Caller(1, lambda x, _: (-x[0], [], None)),
    "-=": Caller(2, lambda x, _: (None, [(0, x[0] - x[1], False)], None)),
    "--=": Caller(2, lambda x, _: (None, [(0, -x[0], False)], None)),
    "-!": Caller(2, lambda x, _: (abs(x[0] - x[1]), [], None)),
    "-=!": Caller(2, lambda x, _: (None, [(0, abs(x[0] - x[1]), False)], None)),
    "/": Caller(2, lambda x, _: (x[0] / x[1], [], None)),
    "/=": Caller(2, lambda x, _: (None, [(0, x[0] / x[1], False)], None)),
    "%": Caller(2, lambda x, _: (x[0] % x[1], [], None)),
    "%=": Caller(2, lambda x, _: (None, [(0, x[0] % x[1], False)], None)),

    "if:": Caller(1, lambda x, _: (None, [], None if x[0] else 0)),
    "if::": Caller(1, lambda x, _: (None, [], None if x[0] else 0)),
    "else": Caller(0, lambda x, _: (None, [], 0)),
    "while:": Caller(1, lambda x, _: (None, [], None if x[0] else 0)),
    ":ihw": Caller(0, lambda x, _: (None, [], 0)),

    # * TYPES
    "->str": Caller(1, lambda x, _: (str(x[0]), [], None)),
    "->int": Caller(1, lambda x, _: (int(x[0]), [], None)),
    "->ord": Caller(1, lambda x, _: (ord(x[0]), [], None)),
    "->chr": Caller(1, lambda x, _: (chr(x[0]), [], None)),
    "->cpx": Caller(2, lambda x, _: (complex(x[0], x[1]), [], None)),
    "->dec": Caller(1, lambda x, _: (float(x[0]), [], None)),
    "->lst": Caller(1, lambda x, _: (list(x[0]), [], None)),

    "[": Caller(-1, lambda x, _: (x, [], None)),
    "@": Caller(2, lambda x, _: (x[0][x[1]], [], None)),
    "@<-": Caller(2, lambda x, _: (None, [(0, x[0][:x[1]] + x[2] + x[0][x[1] + 1:], False)], None)),

    # * LIST & STRING MANIPULATION

    "rev": Caller(1, lambda x, _: (x[::-1], [], None)),
    "sort": Caller(1, lambda x, _: (sort(x[0]), [], None)),
    "rep": Caller(1, lambda x, _: (x[0] * x[1], [], None)),
    "lst": Caller(1, lambda x, _: (x[0][-1], [], None)),
    "fst": Caller(1, lambda x, _: (x[0][0], [], None)),

    "/S": Caller(1, lambda x, _: (list(x[0]), [], None)),
    "wS": Caller(1, lambda x, _: (x[0].split(), [], None)),
    ",S": Caller(1, lambda x, _: (x[0].split(","), [], None)),

    "map": Caller(2, lambda x, table: (map_over(x[0], x[1], table), [], None)),

    # * ARITHMETIC FUNCTIONS
    "divs": Caller(2, lambda x, _: (x[1] % x[0] == 0, [], None)),
})
