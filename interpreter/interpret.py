from copy import deepcopy as copy

from interpreter.util_classes import Caller, Env, Anchor, VarEntry, CallerEntry
from interpreter.builtins import BUILTINS_TABLE
from interpreter.lex import tokenize, Token


def get_anchors(tokens: list[Token]):
    # !TODO: rewrite anchor detection

    kw_stack: list[tuple[int, str]] = []
    anchors: dict[int, Anchor] = {}
    for i in range(len(tokens)):
        kw = tokens[i].value
        if kw == "else":
            while len(kw_stack) >= 0 and kw_stack[-1][1] != "if::":
                anchors[kw_stack[-1][0]].add_jump(i)  # implicitly ends other things
                kw_stack.pop()
            if len(kw_stack) > 0:
                anchors[kw_stack[-1][0]].add_jump(i)
            anchors[i] = Anchor()
            kw_stack.append((i, kw))
        elif kw == ":fi":
            while len(kw_stack) > 0 and kw_stack[-1][1] == "else":
                anchors[kw_stack[-1][0]].add_jump(i)
                kw_stack.pop()
            anchors[kw_stack[-1][0]].add_jump(i)
            kw_stack.pop()
        elif kw == ":ihw":
            while len(kw_stack) > 0 and kw_stack[-1][1] != "while:":
                anchors[kw_stack[-1][0]].add_jump(i)
                kw_stack.pop()
            anchors[kw_stack[-1][0]].add_jump(i)
            anchors[i] = Anchor(jump_to=[kw_stack[-1][0] - 1])
            kw_stack.pop()
        elif kw == ":*!":
            if len(kw_stack) > 0:
                for k in kw_stack:
                    anchors[k[0]].add_jump(i)
                kw_stack = []
        elif kw in ["if:", "if::", "while:"]:
            kw_stack.append((i, kw))
            anchors[i] = Anchor()
    while len(kw_stack) > 0:
        anchors[kw_stack[-1][0]].add_jump(len(tokens))
        kw_stack.pop()
    return anchors


class Interpreter:
    def __init__(self, string: str, table=None):
        self.tokens = tokenize(string)
        self.i = 0
        self.table = Env()
        if table is None:
            self.table.prev = copy(BUILTINS_TABLE)
        else:
            self.table.prev = copy(table)
        self.var_stack: list[list[VarEntry]] = [[]]
        self.call_stack: list[CallerEntry] = []
        self.anchors = get_anchors(self.tokens)

    def fill_args(self):
        self.call_stack[-1].caller.add_args([ve.value for ve in self.var_stack[-1]])

    def resolve(self):
        cal = self.call_stack[-1]
        var = self.var_stack[-1]
        (ret, write_list, jump) = cal.caller.resolve(self.table)
        self.var_stack.pop()
        self.call_stack.pop()
        if ret is not None:
            self.var_stack[-1].append(VarEntry(Token(Token.VAL, ret), ret))
        for (idx, obj, frc) in write_list:
            if frc:
                self.table.force_def(var[idx].token.value, obj)
            else:
                self.table.set(var[idx].token.value, obj)
        if jump is not None:
            self.i = self.anchors[cal.pos].jump_to[jump]

    def handle_kw(self, kw: str):
        if kw == ";!":
            self.fill_args()
            self.var_stack.pop()
            self.var_stack[-1].append(VarEntry(self.call_stack[-1].token, self.call_stack[-1].caller))
            self.call_stack.pop()
        elif kw == ";":
            self.fill_args()
            self.call_stack[-1].caller.enclose()
            self.resolve()
        elif kw == "{":
            self.table = Env(p=self.table)
        elif kw == "}":
            self.table = self.table.prev

    def run(self):
        tokens = self.tokens
        while self.i < len(tokens):
            i = self.i
            t = tokens[i]
            if t.kind == Token.VAL:
                self.var_stack[-1].append(VarEntry(t, t.value))
            elif t.kind == Token.ID:
                c = self.table.get(t.value)
                if type(c) == Caller:
                    self.call_stack.append(CallerEntry(i, t, copy(c)))
                    self.var_stack.append([])
                else:
                    self.var_stack[-1].append(VarEntry(t, copy(c)))
            elif t.kind == Token.KW:
                self.handle_kw(t.value)

            # RESOLVE ALL FULFILLED CALLERS
            while len(self.call_stack) > 0 and len(self.var_stack[-1]) == self.call_stack[-1].caller.args_left():
                self.fill_args()
                self.resolve()
            self.i += 1

        # IMPLICIT ENCLOSING AT THE END
        for _ in range(len(self.call_stack)):
            self.call_stack[-1].caller.add_args([ve.value for ve in self.var_stack[-1]])
            self.call_stack[-1].caller.enclose()
            self.resolve()

        # IMPLICIT OUTPUT
        return ", ".join([str(ve.value) for ve in self.var_stack[0]])
