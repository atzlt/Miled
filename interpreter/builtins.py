import random
from copy import deepcopy as copy
from fractions import Fraction
from math import *
from interpreter.util_classes import Caller, Env, Token, C, R
from functions.num_theory import *
from primality import primality as prime
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
    return R(c)
def pop_at(x, t):
    c = x[0][1][x[1][1]]
    t.set(x[0][0], x[0][1][:x[1][1]] + x[0][1][x[1][1] + 1:])
    return R(c)
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
            table.force_def(param_list[j] + suffix, param[j])
        ret = Interpreter(code, table, None).run()
        return R(ret)

    return Caller(
        len(param_list),
        run_new_caller
    )
def map_over(f: Caller, old_list: list, table: Env):
    return [
        copy(f).add_args([(None, i)]).enclose().resolve(table).ret
        for i in old_list
    ]
BUILTINS_TABLE = Env(table={
    "<-": C(2, lambda x, t: R(t.s(x[0][0], x[1][1]))),
    ":=": C(2, lambda x, t: R(t.d(x[0][0], x[1][1]))),
    "~": C(-1, lambda x, _: R(x[-1][1])),
    "o>": C(1, lambda x, _: R(print(x[0][1]))),

    "def": C(3, lambda x, t: R(t.d(x[0][0], def_new_caller(x[1][1], x[2][1])))),
    "fn": C(2, lambda x, t: R(def_new_caller(x[0][1], x[1][1]))),

    ">": C(2, lambda x, _: R(x[0][1] > x[1][1])),
    "<": C(2, lambda x, _: R(x[0][1] < x[1][1])),
    ">=": C(2, lambda x, _: R(x[0][1] >= x[1][1])),
    "<=": C(2, lambda x, _: R(x[0][1] >= x[1][1])),
    "!=": C(2, lambda x, _: R(x[0][1] != x[1][1])),
    "!": C(1, lambda x, _: R(not x[0][1])),
    "=!": C(1, lambda x, t: R(t.s(x[0][0], not x[0][1]))),
    "&": C(2, lambda x, _: R(x[0][1] and x[1][1])),
    "&=": C(2, lambda x, t: R(t.s(x[0][0], x[0][1] and x[1][1]))),
    "|": C(2, lambda x, _: R(x[0][1] or x[1][1])),
    "|=": C(2, lambda x, t: R(t.s(x[0][0], x[0][1] or x[1][1]))),
    "==": C(2, lambda x, _: R(x[0][1] == x[1][1])),

    "+": C(2, lambda x, _: R(x[0][1] + x[1][1])),
    "+=": C(2, lambda x, t: R(t.s(x[0][0], x[0][1] + x[1][1]))),
    "n+": C(-1, lambda x, _: R(sum(v(x)))),
    "*": C(2, lambda x, _: R(x[0][1] * x[1][1])),
    "*=": C(2, lambda x, t: R(t.s(x[0][0], x[0][1] * x[1][1]))),
    "**": C(2, lambda x, _: R(x[0][1] ** x[1][1])),
    "**=": C(2, lambda x, t: R(t.s(x[0][0], x[0][1] ** x[1][1]))),
    "n*": C(-1, lambda x, _: R(product(v(x)))),
    "-": C(2, lambda x, _: R(x[0][1] - x[1][1])),
    "0-": C(1, lambda x, _: R(-x[0][1])),
    "-=": C(2, lambda x, t: R(t.s(x[0][0], x[0][1] - x[1][1]))),
    "0-=": C(1, lambda x, t: R(t.s(x[0][0], -x[0][1]))),
    "-!": C(2, lambda x, _: R(abs(x[0][1] - x[1][1]))),
    "-=!": C(2, lambda x, t: R(t.s(x[0][0], abs(x[0][1] - x[1][1])))),
    "/": C(2, lambda x, _: R(x[0][1] / x[1][1])),
    "/=": C(2, lambda x, t: R(t.s(x[0][0], x[0][1] / x[1][1]))),
    "//": C(2, lambda x, _: R(x[0][1] // x[1][1])),
    "//=": C(2, lambda x, t: R(t.s(x[0][0], x[0][1] // x[1][1]))),
    "%": C(2, lambda x, _: R(x[0][1] % x[1][1])),
    "%=": C(2, lambda x, t: R(t.s(x[0][0], x[0][1] % x[1][1]))),
    "sum": C(1, lambda x, _: R(sum(x[0][1]))),
    "prd": C(1, lambda x, _: R(product(x[0][1]))),
    "^^": C(1, lambda x, _: R(x[0][1] ^ x[1][1])),
    "||": C(1, lambda x, _: R(x[0][1] | x[1][1])),
    "&&": C(1, lambda x, _: R(x[0][1] & x[1][1])),

    "if:": C(1, lambda x, _: R(None, None if x[0][1] else 0)),
    "if::": C(1, lambda x, _: R(None, None if x[0][1] else 0)),
    "else": C(0, lambda x, _: R(None, 0)),
    "while:": C(1, lambda x, _: R(None, None if x[0][1] else 0)),
    ":ihw": C(0, lambda x, _: R(None, 0)),

    # * TYPES
    "->str": C(1, lambda x, _: R(str(x[0][1]))),
    "->int": C(1, lambda x, _: R(int(x[0][1]))),
    "->ord": C(1, lambda x, _: R(ord(x[0][1]))),
    "->chr": C(1, lambda x, _: R(chr(x[0][1]))),
    "->dec": C(1, lambda x, _: R(float(x[0][1]))),
    "->lst": C(1, lambda x, _: R(list(x[0][1]))),
    "->frc": C(1, lambda x, _: R(Fraction(x[0][1]))),

    "bin": C(1, lambda x, _: R(bin(x[0][1]))),
    "oct": C(1, lambda x, _: R(oct(x[0][1]))),
    "hex": C(1, lambda x, _: R(hex(x[0][1]))),
    "frc": C(2, lambda x, _: R(Fraction(x[0][1], x[1][1]))),
    "cpx": C(2, lambda x, _: R(complex(x[0][1], x[1][1]))),

    # For Fraction
    "limden": C(1, lambda x, _: R(x[0][1].limit_denominator())),
    "limden=": C(2, lambda x, _: R(x[0][1].limit_denominator(x[1][1]))),

    # * LIST & STRING MANIPULATION

    "[": C(-1, lambda x, _: R([el[1] for el in x])),
    "@": C(2, lambda x, _: R(x[0][1][x[1][1]])),
    "@<-": C(3, lambda x, t: R(t.s(x[0][0], x[0][1][:x[1][1]] + x[2][1] + x[0][1][x[1][1] + 1:]))),
    "+@": C(3, lambda x, t: R(t.s(x[0][0], x[0][1][:x[1][1]] + [x[2][1]] + x[0][1][x[1][1]:]))),
    "-@": C(2, pop_at),
    "@?": C(2, lambda x, _: R(x[0][1].find(x[1][1]))),
    "in": C(2, lambda x, _: R(x[0][1] in x[1][1])),

    "rev": C(1, lambda x, _: R(x[::-1])),
    "sort": C(1, lambda x, _: R(sort(x[0][1]))),
    "lst": C(1, lambda x, _: R(x[0][1][-1])),
    "fst": C(1, lambda x, _: R(x[0][1][0])),
    "len": C(1, lambda x, _: R(len(x[0][1]))),
    "push": C(2, lambda x, t: R(t.s(x[0][0], x[0][1] + [x[1][1]]))),
    "pushto": C(2, lambda x, t: R(t.s(x[1][0], x[1][1] + [x[0][1]]))),
    "pop": C(1, pop),
    "[:]": C(3, lambda x, _: R(x[0][1][x[1][1]:x[2][1]])),
    "[::]": C(4, lambda x, _: R(x[0][1][x[1][1]:x[2][1]:x[3][1]])),
    "prf": C(1, lambda x, _: R([x[0][1][:i] for i in range(1, len(x[0][1]) + 1)])),
    "!prf": C(1, lambda x, _: R([x[0][1][:i] for i in range(1, len(x[0][1]))])),
    "suf": C(1, lambda x, _: R([x[0][1][:i] for i in range(len(x[0][1]))])),
    "!suf": C(1, lambda x, _: R([x[0][1][:i] for i in range(1, len(x[0][1]))])),
    "CAP": C(1, lambda x, _: R(x[0][1].upper())),
    "low": C(1, lambda x, _: R(x[0][1].lower())),
    "CAP?": C(1, lambda x, _: R(x[0][1].isupper())),
    "low?": C(1, lambda x, _: R(x[0][1].islower())),
    "Cap": C(1, lambda x, _: R(x[0][1].capitalize())),
    "ctr": C(2, lambda x, _: R(x[0][1].center(x[1][1]))),
    "ctr=": C(3, lambda x, _: R(x[0][1].center(x[1][1], x[2][1]))),
    "cnt": C(2, lambda x, _: R(x[0][1].count(x[1][1]))),
    "alnum?": C(1, lambda x, _: R(x[0][1].isalnum())),
    "alp?": C(1, lambda x, _: R(x[0][1].isalpha())),
    "ascii?": C(1, lambda x, _: R(x[0][1].isascii())),
    "dec?": C(1, lambda x, _: R(x[0][1].isdecimal())),
    "dgt?": C(1, lambda x, _: R(x[0][1].isdigit())),
    "print?": C(1, lambda x, _: R(x[0][1].isprintable())),
    "title?": C(1, lambda x, _: R(x[0][1].istitle())),
    "sp?": C(1, lambda x, _: R(x[0][1].isspace())),
    "sub": C(3, lambda x, _: R(x[0][1].replace(x[1][1], x[2][1]))),
    "sub#": C(4, lambda x, _: R(x[0][1].replace(x[1][1], x[2][1], x[3][1]))),
    "pad": C(2, lambda x, _: R(x[0][1].rjust(x[1][1]))),
    "pad=": C(3, lambda x, _: R(x[0][1].rjust(x[1][1], x[2][1]))),
    "lpad": C(2, lambda x, _: R(x[0][1].ljust(x[1][1]))),
    "lpad=": C(3, lambda x, _: R(x[0][1].ljust(x[1][1], x[2][1]))),
    "zfil": C(2, lambda x, _: R(x[0][1].zfill(x[1][1]))),
    "trm": C(2, lambda x, _: R(x[0][1].strip(x[1][1]))),
    "trm=": C(3, lambda x, _: R(x[0][1].strip(x[1][1], x[2][1]))),
    "rtrm": C(2, lambda x, _: R(x[0][1].rstrip(x[1][1]))),
    "rtrm=": C(3, lambda x, _: R(x[0][1].rstrip(x[1][1], x[2][1]))),
    "ltrm": C(2, lambda x, _: R(x[0][1].lstrip(x[1][1]))),
    "ltrm=": C(3, lambda x, _: R(x[0][1].lstrip(x[1][1], x[2][1]))),

    "..<": C(2, lambda x, t: R(list(range(x[0][1], x[1][1])))),
    "..=": C(2, lambda x, t: R(list(range(x[0][1], x[1][1] + 1)))),
    ":.<": C(3, lambda x, t: R(list(range(x[0][1], x[1][1], x[2][1])))),

    "cS": C(1, lambda x, _: R(list(x[0][1]))),
    "wS": C(1, lambda x, _: R(x[0][1].split())),
    "lS": C(1, lambda x, _: R(x[0][1].splitlines())),
    ",S": C(1, lambda x, _: R(x[0][1].split(","))),
    "S=": C(2, lambda x, _: R(x[0][1].split(x[1][1]))),
    "rS=": C(2, lambda x, _: R(x[0][1].rsplit(x[1][1]))),

    "join": C(2, lambda x, _: R(x[0][1].join(x[1][1]))),

    "map": C(2, lambda x, t: R(map_over(x[0][1], x[1][1], t))),

    # * MORE FUNCTIONS
    # * Math
    "max": C(2, lambda x, _: R(max(x[0][1], x[1][1]))),
    "min": C(2, lambda x, _: R(min(x[0][1], x[1][1]))),
    "nmax": C(-1, lambda x, _: R(max([el[1] for el in x]))),
    "nmin": C(2, lambda x, _: R(min([el[1] for el in x]))),
    "lmax": C(1, lambda x, _: R(max(x[0][1]))),
    "lmin": C(1, lambda x, _: R(min(x[0][1]))),
    "abs": C(1, lambda x, _: R(abs(x[0][1]))),
    "sqrt": C(1, lambda x, _: R(sqrt(x[0][1]))),
    "sin": C(1, lambda x, _: R(sin(x[0][1]))),
    "cos": C(1, lambda x, _: R(cos(x[0][1]))),
    "ln": C(1, lambda x, _: R(log(x[0][1], e))),
    "flr": C(1, lambda x, _: R(floor(x[0][1]))),
    "ceil": C(1, lambda x, _: R(ceil(x[0][1]))),
    "rnd": C(1, lambda x, _: R(round(x[0][1]))),
    "PI": pi,
    "EE": e,
    "II": 1j,
    "#bit": C(1, lambda x, _: R(x[0][1].bit_length())),
    "#1bt": C(1, lambda x, _: R(x[0][1].bit_count())),
    "rand": C(0, lambda _, __: R(random.random())),
    "rand#": C(1, lambda x, _: R(random.randint(0, x[0][1]))),

    # * Number-Theoretic
    "#:#": C(1, lambda x, _: R(x[0][1].as_integer_ratio())),
    "div": C(2, lambda x, _: R(x[1][1] % x[0][1] == 0)),
    "gcd": C(2, lambda x, _: R(gcd(x[0][1], x[1][1]))),
    "ngcd": C(-1, lambda x, _: R(gcd(*v(x)))),
    "lgcd": C(1, lambda x, _: R(gcd(*x[0][1]))),
    "lcm": C(2, lambda x, _: R(lcm(x[0][1], x[1][1]))),
    "nlcm": C(-1, lambda x, _: R(lcm(*v(x)))),
    "llcm": C(1, lambda x, _: R(lcm(*x[0][1]))),
    "prim?": C(1, lambda x, _: R(prime.isprime(x[0][1]))),
    "prim@": C(1, lambda x, _: R(prime.nthprime(x[0][1]))),
    "prim]": C(1, lambda x, _: R(prime.prange(x[0][1]))),
    "pFctS": C(1, lambda x, _: R(prime_factors(x[0][1], option="set"))),
    "pFctM": C(1, lambda x, _: R(prime_factors(x[0][1], option="multi"))),
    "pFctE": C(1, lambda x, _: R(prime_factors(x[0][1], option="exp"))),
    "#pFct": C(1, lambda x, _: R(len(prime_factors(x[0][1], option="set")))),
    "#pFctM": C(1, lambda x, _: R(len(prime_factors(x[0][1], option="multi")))),
    "divs": C(1, lambda x, _: R(divisors(x[0][1]))),
    "#divs": C(1, lambda x, _: R(divisor_tau(x[0][1]))),
    "divsum": C(1, lambda x, _: R(divisor_sigma(x[0][1]))),
    "eulPhi": C(1, lambda x, _: R(euler_phi(x[0][1]))),
    "coprm": C(1, lambda x, _: R(coprime_numbers(x[0][1]))),
})
