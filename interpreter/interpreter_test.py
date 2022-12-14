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
            [t.value for t in tokenize(r':= str "\"Hello world!\"" str')]
        )
        self.assertEqual(
            [":=", "x\"y", "a", "x\"y"],
            [t.value for t in tokenize(":= x\"y \"a\" x\"y")]
        )
        self.assertEqual(
            ["if:", "if:", "if:", "if::", "if:", "else", ":fi", ":fi", ":fi", ":fi"],
            [t.value for t in tokenize("if: ^3 if:: if: else :fi ^4")]
        )


class InterpreterTestCase(unittest.TestCase):
    def test_anchor(self):
        self.assertEqual(
            [
                [9],
                [8],
                [7],
                [5, 6],
                [5],
                [6]
            ],
            [a.jump_to for a in get_anchors(tokenize("if: ^3 if:: if: else :fi ^4")).values()]
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
        self.assertEqual(
            [
                [6],
                [4],
                [-1]
            ],
            [a.jump_to for a in get_anchors(tokenize("while: <: x while: :> 1 :ihw")).values()]
        )
        self.assertEqual(
            [
                [31]
            ],
            [a.jump_to for a in get_anchors(tokenize(
                "def g [ \"n\" ; <: := x 1 ~ map fn [] <: += x / - cos x x + 1 sin x :> ..< 0 n x ; :>"
            )).values()]
        )

    def test_interpreter(self):
        self.assertEqual(
            True,
            Interpreter("<- x n+ ;! > x 1 ; 0").run()
        )
        self.assertEqual(
            3,
            Interpreter("<- x + 1 ;! <- y x 2 y").run()
        )
        self.assertEqual(
            "\\\"Hello, world!\"",
            Interpreter(":= str \"\\\\\\\"Hello, world!\\\"\" str").run()
        )
        self.assertEqual(
            3,
            Interpreter("<- x n+ ;! <- x ;! x 1 ;! { x 2 ; }").run()
        )
        self.assertEqual(
            2,
            Interpreter("if:: ~ <- x n+ ;! > x 1 ; 0 ; <- y + 1 ;! y 1 else 0").run()
        )
        self.assertEqual(
            3,
            Interpreter("if:: if:: false true else false :fi 2 else 3").run()
        )
        self.assertEqual(
            3,
            Interpreter(":= x 3 { := x 4 } x").run()
        )
        self.assertEqual(
            3,
            Interpreter(":= x 4 { <- x 3 } x").run()
        )
        self.assertEqual(
            100,
            Interpreter(":= x 100 := y 0 while: != x 0 -= x 1 += y 1 :ihw y").run()
            # Also tested when replaced by 1000000, slower than expected (~1min) :(
        )
        self.assertEqual(
            2**100,
            Interpreter(":= x 101 := y n* ;! while: ~ -= x 1 != x 0 ; <- y ;! y 2 ;! :ihw y ;").run()
        )
        self.assertEqual(
            # A FizzBuzz Example
            "\n".join([
                "FizzBuzz" if i % 3 == 0 and i % 5 == 0 else
                "Fizz" if i % 3 == 0 else
                "Buzz" if i % 5 == 0
                else str(i)
                for i in range(1, 101)
            ]),
            Interpreter(r"""
            join "\n"
                map fn cS "x" <:
                    if:: div 15 x "FizzBuzz"
                    else if:: div 3 x "Fizz"
                    else if:: div 5 x "Buzz"
                    else ->str x
                :> ..= 1 100
            """).run()
        )
        self.assertEqual(
            23,
            Interpreter(":= x [ 1 2 3 ; ->int + ->str @ x 1 ->str @ x 2").run()
        )
        self.assertEqual(
            [1, 1],
            Interpreter(":= x [ 1 2 3 ; ~ pop x pop x pushto 1 x x ;").run()
        )
        self.assertEqual(
            3,
            Interpreter("def x ,S \"y,z,w\" <: n+ y z w ; :> x 1 1 1").run()
        )
        self.assertEqual(
            [2, 3, 4],
            Interpreter("def f [ \"x\" ; <: + x 1 :> := x [ 1 2 3 ; map f ;! x").run()
        )
        self.assertEqual(
            [2, 3, 4],
            Interpreter(":= x [ 1 2 3 ; map fn cS \"x\" <: + x 1 :> x").run()
        )
        self.assertEqual(
            3,
            Interpreter(":= x [ 1 2 3 ; := y 0 ~ map fn [] <: += y 1 :> x y ;").run()
        )
        self.assertEqual(
            # Euclid Algorithm
            1,
            Interpreter(r"""
            def myGcd cS "xy" <:
                if:: div min x y max x y min x y
                else gcd min x y % max x y min x y :fi
            :>
            def myLGcd "x" <:
                while: >= len x 2 pushto myGcd pop x pop x x :ihw
                @ x 0
            :>
            myLGcd [ 63245986 102334155 ;
            """).run()
        )
        self.assertEqual(
            10,
            Interpreter("@ @ pFctE ** 4 5 0 1").run()
        )
        self.assertEqual(
            # Factorial example
            120,
            Interpreter(r"""
            def factorial cS "x" <:
                if:: == x 1 1
                else * x factorial - x 1
            :>
            factorial 5
            """).run()
        )
        self.assertEqual(
            [2, 4, 3],
            Interpreter(":= x [ 1 2 3 ; ~ -@ x 0 +@ x 1 4 x ;").run()
        )
        self.assertAlmostEqual(
            0.7390851332151607,
            Interpreter(r"""
            def g [ "n" ; <: := x 1 ~ map fn [] <: += x / - cos x x + 1 sin x :> ..< 0 n x ; :>
            g 10
            """).run()
        )


if __name__ == "__main__":
    unittest.main()
