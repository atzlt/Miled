import unittest

from interpreter.interpret import interpret, get_anchors
from interpreter.lex import tokenize


class LexTestCase(unittest.TestCase):
    def test_tokenize(self):
        self.assertEqual(
            ["abc", "[", "de\t fg", "hi", "jk", -1.25, "-15k"],
            [t.value for t in tokenize("abc [ \"de\t fg\" hi       jk\n\t -1.25 -15k")]
        )
        self.assertEqual(
            ["let", "x", "+", 3.0, ";!", "x", 3],
            [t.value for t in tokenize("let x + 3.0 ;! x 3")]
        )


class InterpreterTestCase(unittest.TestCase):
    def test_anchor(self):
        self.assertEqual(
            [
                [7],
                [7],
                [7],
                [5, 6],
                [5],
                [6]
            ],
            [a.jump_to for a in get_anchors(tokenize("if: if: if: if:: if: else :fi :*!")).values()]
        )
        self.assertEqual(
            [
                [8, 10],
                [4, 6],
                [6],
                [10]
            ],
            [a.jump_to for a in get_anchors(tokenize("if:: if:: false true else false :fi 2 else 3")).values()]
        )
        self.assertEqual(
            [
                [16],
                [5]
            ],
            [a.jump_to for a in get_anchors(tokenize("set x 3 set y 0 while: x != 0 -= x 1 += y 1 :ihw y")).values()]
        )

    def test_interpreter(self):
        self.assertEqual(
            "True",
            interpret("let x n+ ;! > x 1 ; 0")
        )
        self.assertEqual(
            "3",
            interpret("let x + 1 ;! let y x 2 y")
        )
        self.assertEqual(
            "3",
            interpret("let x n+ ;! let \"x\" x 1 ;! { x 2 ; }")
        )
        self.assertEqual(
            "2",
            interpret("if:: ~ let x n+ ;! > x 1 ; 0 ; let y + 1 ;! y 1 else 0")
        )
        self.assertEqual(
            "3",
            interpret("if:: if:: false true else false :fi 2 else 3")
        )
        self.assertEqual(
            "3",
            interpret("if: true :fi 3")
        )
        self.assertEqual(
            "3",
            interpret("set x 3 { set x 4 } x")
        )
        self.assertEqual(
            "3",
            interpret("set x 4 { let x 3 } x")
        )
        self.assertEqual(
            "3",
            interpret("set x 3 set y 0 while: != x 0 -= x 1 += y 1 :ihw y")
        )


if __name__ == "__main__":
    unittest.main()
