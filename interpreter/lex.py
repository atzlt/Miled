import re


class Token:
    VAL = 1
    ID = 2
    KW = 3

    def __init__(self, kind: int, value=None):
        self.kind = kind
        self.value = value


def is_float(string: str):
    if re.match(r"^-?[0-9]+\.[0-9]+$", string):
        return True


def is_int(string: str):
    if re.match("^-?[0-9]+$", string):
        return True


KEYWORDS = [
    ";!", ";",  # TERMINATION
    "def",  # CALLER DECLARATION
    ":fi", ":*!",  # END MARKERS
    "{", "}",  # SCOPE MARKERS
]


def tokenize(string: str) -> list[Token]:  # !TODO: rewrite tokenizer
    string += " "
    i = 0
    t = []
    buf = ""
    str_flag = False
    while i < len(string):
        if string[i] == "\"":
            str_flag = not str_flag
        if string[i].isspace() or i == len(string) - 1:
            if str_flag:
                buf += string[i]
                i += 1
                continue
            elif buf == "":
                i += 1
                continue
            else:
                if is_float(buf):
                    t.append(Token(Token.VAL, float(buf)))
                elif is_int(buf):
                    t.append(Token(Token.VAL, int(buf)))
                elif buf == "true":
                    t.append(Token(Token.VAL, True))
                elif buf == "false":
                    t.append(Token(Token.VAL, False))
                elif buf[0] == "\"" and buf[-1] == "\"":
                    t.append(Token(Token.VAL, buf[1:-1]))
                elif buf in KEYWORDS:
                    t.append(Token(Token.KW, buf))
                else:
                    t.append(Token(Token.ID, buf))
                buf = ""
                i += 1
                continue
        else:
            buf += string[i]
            i += 1
    return t
