import re

from interpreter.util_classes import Token, Anchor


def is_float(string: str):
    if re.match(r"^-?[0-9]+\.[0-9]+$", string):
        return True
    return False


def is_int(string: str):
    if re.match("^-?[0-9]+$", string):
        return True
    return False


def is_rep_sym(string: str):
    if string[0] == "^" and is_int(string[1:]):
        return True
    return False


KEYWORDS = [
    ";!", ";",  # TERMINATION
    "<:", ":>",  # PROC MARKERS
    ":fi",  # END MARKERS
    "{", "}",  # SCOPE MARKERS
]


def to_token(buf: str) -> Token:
    if buf[0] == "\"" and buf[-1] == "\"":
        return Token(
            Token.VAL,
            buf[1:-1]
            .replace(r"\"", "\"")
            .replace(r"\\", "\\")
            .replace(r"\n", "\n")
            .replace(r"\t", "\t")
            .replace(r"\r", "\r")
        )
    elif is_int(buf):
        return Token(Token.VAL, int(buf))
    elif is_float(buf):
        return Token(Token.VAL, float(buf))
    elif buf == "true":
        return Token(Token.VAL, True)
    elif buf == "False":
        return Token(Token.VAL, False)
    elif buf == "??":
        return Token(Token.VAL, None)
    elif buf == "[]":
        return Token(Token.VAL, [])
    elif buf in KEYWORDS:
        return Token(Token.KW, buf)
    else:
        return Token(Token.ID, buf)


def tokenize(string: str) -> list[Token]:
    string = string.lstrip()
    string += " "
    i = 0
    t = []
    buf = ""
    flags = {
        "on_word_end": False,
        "in_str": False,
        "escaping": False
    }
    while i < len(string):
        if string[i].isspace():
            if flags["in_str"]:
                buf += string[i]
            else:
                if not flags["on_word_end"]:

                    # * RESOLVING STEP
                    if is_rep_sym(buf):
                        t += [t[-1]] * (int(buf[1:]) - 1)
                    else:
                        t.append(to_token(buf))
                    buf = ""

                flags["on_word_end"] = True
        elif string[i] == "\\":
            if flags["in_str"]:
                flags["escaping"] = True
            buf += "\\"
        elif string[i] == "\"":
            if not flags["escaping"]:
                if flags["on_word_end"]:
                    flags["in_str"] = True
                    flags["on_word_end"] = False
                elif i == len(string) - 1 or string[i + 1].isspace():
                    flags["in_str"] = False
            buf += "\""
            flags["escaping"] = False
        else:
            flags["on_word_end"] = False
            flags["escaping"] = False
            buf += string[i]
        i += 1
    return t


def get_anchors(tokens: list[Token]):
    # !TODO: cleanup anchor detection

    proc_depth = 0
    kw_stack: list[tuple[int, str]] = []
    anchors: dict[int, Anchor] = {}
    for i in range(len(tokens)):
        kw = tokens[i].value

        if proc_depth == 0:
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

            elif kw in ["if:", "if::", "while:"]:
                kw_stack.append((i, kw))
                anchors[i] = Anchor()

            elif kw == "<:":
                kw_stack.append((i, kw))
                anchors[i] = Anchor()
                proc_depth += 1

        else:
            # proc depth > 0 means we're inside a function definition, where we should jump to the matching end
            if kw == "<:":
                proc_depth += 1
            elif kw == ":>":
                proc_depth -= 1
                if proc_depth == 0:
                    while len(kw_stack) > 0 and kw_stack[-1][1] != "<:":
                        anchors[kw_stack[-1][0]].add_jump(i)
                        kw_stack.pop()
                    anchors[kw_stack[-1][0]].add_jump(i)
                    kw_stack.pop()
    while len(kw_stack) > 0:
        anchors[kw_stack[-1][0]].add_jump(len(tokens))
        kw_stack.pop()
    return anchors
