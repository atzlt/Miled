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
def pop(x, t):
    c = x[0][1][-1]
    t.set(x[0][0], x[0][1][:-1])
    return c, None
def def_new_caller(param_list: list[str], code: list[Token]):
    call_id = str(random.randint(0, 65535))
    suffix = "$call_arg$" + call_id
    for i in range(len(code)):
        if code[i].kind == Token.ID and code[i].value in param_list:
            code[i].value += suffix

    def run_new_caller(param: list, old_table: Env):
        from interpreter.interpret import Interpreter
        param = [e[1] for e in param]
        table = Env()
        table.prev = old_table
        for j in range(len(param_list)):
            table.force_def(param_list[j] + suffix, param[j])
        ret = Interpreter(code, table, None).run()
        return ret, None

    return Caller(
        len(param_list),
        run_new_caller
    )
def map_over(f: Caller, old_list: list, table: Env):
    return [
        copy(f).add_args([(None, i)]).enclose().resolve(table)[0]
        for i in old_list
    ]
BUILTINS_TABLE = Env(table={
    "<-": Caller(2, lambda x, t: (t.s(x[0][0], x[1][1]), None)),
    ":=": Caller(2, lambda x, t: (t.d(x[0][0], x[1][1]), None)),
    "~": Caller(-1, lambda x, _: (x[-1][1], None)),
    "o>": Caller(1, lambda x, _: (print(x[0][1]), None)),

    "def": Caller(3, lambda x, t: (t.d(x[0][0], def_new_caller(x[1][1], x[2][1])), None)),

    ">": Caller(2, lambda x, _: (x[0][1] > x[1][1], None)),
    "<": Caller(2, lambda x, _: (x[0][1] < x[1][1], None)),
    ">=": Caller(2, lambda x, _: (x[0][1] >= x[1][1], None)),
    "<=": Caller(2, lambda x, _: (x[0][1] >= x[1][1], None)),
    "!=": Caller(2, lambda x, _: (x[0][1] != x[1][1], None)),
    "!": Caller(1, lambda x, _: (not x[0][1], None)),
    "=!": Caller(1, lambda x, t: (t.s(x[0][0], not x[0][1]), None)),
    "&": Caller(2, lambda x, _: (x[0][1] and x[1][1], None)),
    "&=": Caller(2, lambda x, t: (t.s(x[0][0], x[0][1] and x[1][1]), None)),
    "|": Caller(2, lambda x, _: (x[0][1] or x[1][1], None)),
    "|=": Caller(2, lambda x, t: (t.s(x[0][0], x[0][1] or x[1][1]), None)),
    "==": Caller(2, lambda x, _: (x[0][1] == x[1][1], None)),

    "+": Caller(2, lambda x, _: (x[0][1] + x[1][1], None)),
    "+=": Caller(2, lambda x, t: (t.s(x[0][0], x[0][1] + x[1][1]), None)),
    "n+": Caller(-1, lambda x, _: (sum([e[1] for e in x]), None)),
    "*": Caller(2, lambda x, _: (x[0][1] * x[1][1], None)),
    "*=": Caller(2, lambda x, t: (t.s(x[0][0], x[0][1] * x[1][1]), None)),
    "n*": Caller(-1, lambda x, _: (product([e[1] for e in x]), None)),
    "-": Caller(2, lambda x, _: (x[0][1] - x[1][1], None)),
    "--": Caller(1, lambda x, _: (-x[0][1], None)),
    "-=": Caller(2, lambda x, t: (t.s(x[0][0], x[0][1] - x[1][1]), None)),
    "--=": Caller(2, lambda x, t: (t.s(x[0][0], -x[0][1]), None)),
    "-!": Caller(2, lambda x, _: (abs(x[0][1] - x[1][1]), None)),
    "-=!": Caller(2, lambda x, t: (t.s(x[0][0], abs(x[0][1] - x[1][1])), None)),
    "/": Caller(2, lambda x, _: (x[0][1] / x[1][1], None)),
    "/=": Caller(2, lambda x, t: (t.s(x[0][0], x[0][1] / x[1][1]), None)),
    "%": Caller(2, lambda x, _: (x[0][1] % x[1][1], None)),
    "%=": Caller(2, lambda x, t: (t.s(x[0][0], x[0][1] % x[1][1]), None)),

    "max": Caller(2, lambda x, _: (max(x[0][1], x[1][1]), None)),
    "min": Caller(2, lambda x, _: (min(x[0][1], x[1][1]), None)),
    "nmax": Caller(-1, lambda x, _: (max([e[1] for e in x]), None)),
    "nmin": Caller(2, lambda x, _: (min([e[1] for e in x]), None)),
    "lmax": Caller(1, lambda x, _: (max(x[0][1]), None)),
    "lmin": Caller(1, lambda x, _: (min(x[0][1]), None)),

    "if:": Caller(1, lambda x, _: (None, None if x[0][1] else 0)),
    "if::": Caller(1, lambda x, _: (None, None if x[0][1] else 0)),
    "else": Caller(0, lambda x, _: (None, 0)),
    "while:": Caller(1, lambda x, _: (None, None if x[0][1] else 0)),
    ":ihw": Caller(0, lambda x, _: (None, 0)),

    # * TYPES
    "->str": Caller(1, lambda x, _: (str(x[0][1]), None)),
    "->int": Caller(1, lambda x, _: (int(x[0][1]), None)),
    "->ord": Caller(1, lambda x, _: (ord(x[0][1]), None)),
    "->chr": Caller(1, lambda x, _: (chr(x[0][1]), None)),
    "->cpx": Caller(2, lambda x, _: (complex(x[0][1], x[1][1]), None)),
    "->dec": Caller(1, lambda x, _: (float(x[0][1]), None)),
    "->lst": Caller(1, lambda x, _: (list(x[0][1]), None)),

    "[": Caller(-1, lambda x, _: ([e[1] for e in x], None)),
    "@": Caller(2, lambda x, _: (x[0][1][x[1][1]], None)),
    "@<-": Caller(3, lambda x, t: (t.s(x[0][0], x[0][1][:x[1][1]] + x[2][1] + x[0][1][x[1][1] + 1:]), None)),

    # * LIST & STRING MANIPULATION

    "rev": Caller(1, lambda x, _: (x[::-1], None)),
    "sort": Caller(1, lambda x, _: (sort(x[0][1]), None)),
    "rep": Caller(1, lambda x, _: (x[0][1] * x[1][1], None)),
    "lst": Caller(1, lambda x, _: (x[0][1][-1], None)),
    "fst": Caller(1, lambda x, _: (x[0][1][0], None)),
    "len": Caller(1, lambda x, _: (len(x[0][1]), None)),
    "push": Caller(2, lambda x, t: (t.s(x[0][0], x[0][1] + [x[1][1]]), None)),
    "pushto": Caller(2, lambda x, t: (t.s(x[1][0], x[1][1] + [x[0][1]]), None)),
    "pop": Caller(1, pop),

    "/S": Caller(1, lambda x, _: (list(x[0][1]), None)),
    "wS": Caller(1, lambda x, _: (x[0][1].split(), None)),
    ",S": Caller(1, lambda x, _: (x[0][1].split(","), None)),

    "map": Caller(2, lambda x, t: (map_over(x[0][1], x[1][1], t), None)),

    # * ARITHMETIC FUNCTIONS
    "div": Caller(2, lambda x, _: (x[1][1] % x[0][1] == 0, None)),
})
