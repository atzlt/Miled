import random
from copy import deepcopy as copy

from interpreter.util_classes import Token, Env, Caller, ReturnValue


def v(x):
    return [el[1] for el in x]


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
    return ReturnValue(c)


def pop_at(x, t):
    c = x[0][1][x[1][1]]
    t.set(x[0][0], x[0][1][:x[1][1]] + x[0][1][x[1][1] + 1:])
    return ReturnValue(c)


def def_new_caller(param_list: list[str], code: list[Token]):
    call_id = str(random.randint(0, 65535))
    suffix = "$call_arg$" + call_id
    for i in range(len(code)):
        if code[i].kind == Token.ID and code[i].value in param_list:
            code[i].value += suffix

    def run_new_caller(param: list, old_table: Env):
        from interpreter.interpret import Interpreter
        param = v(param)
        table = Env()
        table.prev = old_table
        for j in range(len(param_list)):
            table.def_here(param_list[j] + suffix, param[j])
        ret = Interpreter(code, table, None).run()
        return ReturnValue(ret)

    return Caller(
        len(param_list),
        run_new_caller
    )


def map_over(f: Caller, old_list: list, table: Env):
    return [
        copy(f).add_args([(None, i)]).enclose().resolve(table).ret
        for i in old_list
    ]
