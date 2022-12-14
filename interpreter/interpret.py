from copy import deepcopy as copy
from typing import Callable

from interpreter.util_classes import Caller, Env, ValEntry
from interpreter.builtins import BUILTINS_TABLE
from interpreter.lex import tokenize, Token, get_anchors


class Interpreter:
    def __init__(
            self,
            code: str | list[Token],
            table: Env = None,
            tokenizer: Callable[[str], list[Token]] | None = tokenize
    ):
        if tokenizer is not None or type(code) == str:
            self.tokens = tokenizer(code)
        else:
            self.tokens = code
        self.table = Env()
        if table is None:
            self.table.prev = copy(BUILTINS_TABLE)
        else:
            self.table = table
        self.var_stack: list[list[ValEntry]] = [[]]
        self.call_stack: list[ValEntry] = []
        self.anchors = get_anchors(self.tokens)
        self.i = 0

    def get_val(self, key: ValEntry):
        if key.id is not None:
            return copy(self.table.get(key.id))
        else:
            return key.value

    def fill_arg(self, enclose=False):
        call_ent = self.call_stack.pop()
        caller: Caller = self.get_val(call_ent)
        var = self.var_stack.pop()
        caller.add_args([(v.id, v.value) for v in var])
        if enclose:
            caller.enclose()
        return caller, call_ent

    def handle_kw(self, kw: Token):
        if kw.value == ";!":
            caller, call_ent = self.fill_arg()
            self.var_stack[-1].append(ValEntry(call_ent.id, self.i, caller))
        elif kw.value == ";":
            self.resolve(enclose=True)
        elif kw.value == "{":
            self.table = Env(p=self.table)
        elif kw.value == "}":
            self.table = self.table.prev
        elif kw.value == "<:":
            j = self.anchors[self.i].jump_to[0]
            self.var_stack[-1].append(ValEntry(None, self.i, self.tokens[self.i + 1:j]))
            self.i = j

    def resolve(self, enclose=False):
        caller, call_ent = self.fill_arg(enclose=enclose)
        ret = caller.resolve(self.table)
        if ret.ret is not None:
            self.var_stack[-1].append(ValEntry(None, self.i, ret.ret))
        if ret.jump is not None:
            self.i = self.anchors[call_ent.pos].jump_to[ret.jump]

    def run_step(self):
        t = self.tokens[self.i]

        if t.kind == Token.VAL:
            self.var_stack[-1].append(ValEntry(None, self.i, t.value))
        elif t.kind == Token.ID:
            if type(self.table.get(t.value)) == Caller:
                self.var_stack.append([])
                self.call_stack.append(ValEntry(t.value, self.i, self.table.get(t.value)))
            else:
                self.var_stack[-1].append(ValEntry(t.value, self.i, self.table.get(t.value)))
        elif t.kind == Token.KW:
            self.handle_kw(t)

        while len(self.call_stack) > 0 and \
                self.get_val(self.call_stack[-1]).args_left() == len(self.var_stack[-1]):
            self.resolve()

        self.i += 1

    def run(self):
        while self.i < len(self.tokens):
            self.run_step()

        if len(self.var_stack[0]) == 0:
            return None
        elif len(self.var_stack[0]) == 1:
            return self.get_val(self.var_stack[0][0])
        else:
            return [self.get_val(v) for v in self.var_stack[0]]
