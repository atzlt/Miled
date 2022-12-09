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


def interpret(string: str, table=None):
    if table is None:
        table = copy(BUILTINS_TABLE)

    tokens = tokenize(string)
    var_stack: list[list[VarEntry]] = [[]]
    call_stack: list[CallerEntry] = []
    anchors = get_anchors(tokens)
    i = 0

    def resolve():
        nonlocal call_stack, var_stack, table, i
        cal = call_stack[-1]
        var = var_stack[-1]
        (ret, write_list, jump) = cal.caller.resolve(table)
        var_stack.pop()
        call_stack.pop()
        if ret is not None:
            var_stack[-1].append(VarEntry(Token(Token.VAL, ret), ret))
        for (idx, frc, obj) in write_list:
            if frc:
                table.set(var[idx].token.value, obj)
            else:
                table.force_def(var[idx].token.value, obj)
        if jump is not None:
            i = anchors[cal.pos].jump_to[jump]

    while i < len(tokens):
        t = tokens[i]
        if t.kind == Token.VAL:
            var_stack[-1].append(VarEntry(t, t.value))
        elif t.kind == Token.ID:
            c = table.get(t.value)
            if type(c) == Caller:
                call_stack.append(CallerEntry(i, t, copy(c)))
                var_stack.append([])
            else:
                var_stack[-1].append(VarEntry(t, copy(c)))
        elif t.kind == Token.KW:
            if t.value == ";!":
                call_stack[-1].caller.add_args([ve.value for ve in var_stack[-1]])
                var_stack.pop()
                var_stack[-1].append(VarEntry(call_stack[-1].token, call_stack[-1].caller))
                call_stack.pop()
            elif t.value == ";":
                call_stack[-1].caller.add_args([ve.value for ve in var_stack[-1]])
                call_stack[-1].caller.enclose()
                resolve()
            elif t.value == "{":
                table = Env(p=table)
            elif t.value == "}":
                table = table.prev

        # RESOLVE ALL FULFILLED CALLERS
        while len(call_stack) > 0 and len(var_stack[-1]) == call_stack[-1].caller.args_left():
            call_stack[-1].caller.add_args([ve.value for ve in var_stack[-1]])
            resolve()
        i += 1

    # IMPLICIT ENCLOSING AT THE END
    while len(call_stack) > 0:
        call_stack[-1].caller.add_args([ve.value for ve in var_stack[-1]])
        call_stack[-1].caller.enclose()
        resolve()

    return ", ".join([str(ve.value) for ve in var_stack[0]])
