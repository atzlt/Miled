from dataclasses import dataclass
from typing import Callable, Self


class Token:
    VAL = 1
    ID = 2
    KW = 3

    def __init__(self, kind: int, value=None):
        self.kind = kind
        self.value = value


@dataclass
class ValEntry:
    id: str | None
    pos: int
    value: any


@dataclass
class ReturnValue:
    ret: any
    jump: int = None


R = ReturnValue  # A shorthand method


class Env:
    def __init__(self, p: Self | None = None, table: dict = None):
        if table is None:
            table = {}
        self.table = table
        self.prev = p

    def get(self, key: str):
        if key in self.table:
            return self.table[key]
        elif self.prev is not None:
            return self.prev.get(key)
        else:
            return None

    def def_here(self, key: str, val):
        self.table[key] = val

    def set(self, key: str, val, origin=True):
        if key in self.table:
            self.table[key] = val
            if not origin:
                return True
        elif self.prev is not None:
            ret = self.prev.set(key, val, origin=False)
            if not ret:
                self.table[key] = val
            if not origin:
                return True
        else:
            if origin:
                self.table[key] = val
            else:
                return False

    s = set
    d = def_here


class Caller:
    """
    A caller instance consists of three parts: arity, arguments and callback. If the number of arguments equals the
    arity ("*fulfilled*"), the caller would be resolved.

    There are two method to return (or resolve) a caller. The first one is "termination". A caller with initial
    arguments same as the arguments present is returned, and it waits for further arguments.

    The second one is "enclosing". If the caller is of fixed arity, the remaining empty slots for arguments are
    filled with `None` and then resolved by the callback function. For non-determinate arity callers. The argument
    list is kept as-is and passed directly to the callback function.

    After the caller is resolved it is **replaced by an immediate value** in the symbol table.
    """
    def __init__(
            self, arity: int,
            callback: Callable[[list[tuple[str, any]], Env | None], ReturnValue]):
        """
        Initialize a caller instance.

        The callback is a function that is called when resolving the caller. The callback should return a tuple: the
        first value is the return value, the third value is the "jump" flag, indicating how the pointer should jump
        according to the anchor.

        :param arity: the expected number or arguments. If set to negative values it accepts unlimited number of
         arguments.

        :param callback: a function that is called when resolving the caller. The callback should return a tuple:
        the first one is the return value; the second one is the "write list", a list about which values in the symbol
        table should change.
        """
        self.callback = callback
        self.arity = arity
        self.args = []

    def is_fulfilled(self):
        return self.arity == len(self.args)

    def args_left(self):
        return self.arity - len(self.args)

    def add_args(self, args: list[tuple[str | None, any]]):
        if self.arity >= 0:
            self.args += args[:self.args_left()]
        else:
            self.args += args
        return self

    def enclose(self):
        if self.arity > 0:
            while not self.is_fulfilled():
                self.add_args([("", None)])
        return self

    def resolve(self, table: Env | None):
        return self.callback(self.args, table)


C = Caller  # A shorthand method


class Anchor:
    def __init__(self, jump_to: list[int] = None):
        if jump_to is None:
            jump_to = []
        self.jump_to = jump_to

    def add_jump(self, dest: int):
        self.jump_to.append(dest)
