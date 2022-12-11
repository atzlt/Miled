import unittest

from interpreter.interpret import Interpreter, get_anchors
from interpreter.lex import tokenize


class LexTestCase(unittest.TestCase):
    def test_tokenize(self):
        self.assertEqual(
            ["abc", "[", "de\t fg", "hi", "jk", -1.25, "-15k"],
            [t.value for t in tokenize("abc [ \"de\t fg\" hi       jk\n\t -1.25 -15k")]
        )
        self.assertEqual(
            [":=", "str", "\"Hello world!\"", "str"],
            [t.value for t in tokenize(":= str \"\\\"Hello world!\\\"\" str")]
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
            [a.jump_to for a in get_anchors(tokenize(":= x 3 := y 0 while: x != 0 -= x 1 += y 1 :ihw y")).values()]
        )

    def test_interpreter(self):
        self.assertEqual(
            "True",
            Interpreter("<- x n+ ;! > x 1 ; 0").run()
        )
        self.assertEqual(
            "3",
            Interpreter("<- x + 1 ;! <- y x 2 y").run()
        )
        self.assertEqual(
            "\\\"Hello, world!\"",
            Interpreter(":= str \"\\\\\\\"Hello, world!\\\"\" str").run()
        )
        self.assertEqual(
            "3",
            Interpreter("<- x n+ ;! <- \"x\" x 1 ;! { x 2 ; }").run()
        )
        self.assertEqual(
            "2",
            Interpreter("if:: ~ <- x n+ ;! > x 1 ; 0 ; <- y + 1 ;! y 1 else 0").run()
        )
        self.assertEqual(
            "3",
            Interpreter("if:: if:: false true else false :fi 2 else 3").run()
        )
        self.assertEqual(
            "3",
            Interpreter(":= x 3 { := x 4 } x").run()
        )
        self.assertEqual(
            "3",
            Interpreter(":= x 4 { <- x 3 } x").run()
        )
        self.assertEqual(
            "100",
            Interpreter(":= x 100 := y 0 while: != x 0 -= x 1 += y 1 :ihw y").run()
            # Also tested when replaced by 1000000, slower than expected (~1min) :(
        )
        self.assertEqual(
            str(2**100),
            Interpreter(":= x 101 := y n* ;! while: ~ -= x 1 != x 0 ; <- y ;! y 2 ;! :ihw y ;").run()
        )
        self.assertEqual(
            # A FizzBuzz Example
            " ".join([
                "FizzBuzz" if i % 3 == 0 and i % 5 == 0 else "Fizz" if i % 3 == 0 else "Buzz" if i % 5 == 0 else str(i)
                for i in range(1, 101)
            ]) + " ",
            Interpreter("""
            := x 0
            := s ""
            while: ~ += x 1 != x 101 ;
                += s if::
                    & divs 3 x divs 5 x "FizzBuzz"
                    else
                        if:: divs 3 x "Fizz"
                        else
                            if:: divs 5 x "Buzz"
                            else ->str x
                            :fi
                        :fi
                    :fi
                += s " "
            :ihw
            s
            """).run()
        )
        self.assertEqual(
            "23",
            Interpreter(":= x [ 1 2 3 ; + ->str _: x 1 ->str _: x 2").run()
        )


if __name__ == "__main__":
    unittest.main()
