from interpreter.interpret import Interpreter
from argparse import ArgumentParser


def try_run(code: str):
    itpr = Interpreter(code)
    try:
        print(itpr.run())
    except Exception as IE:
        print("Cannot run program, an error occurred:")
        print(IE)
        print("near: \"" + str(itpr.tokens[itpr.i].value) + "\" at word #" + str(itpr.i))
        print("Check your code. If you confirm there shouldn't be any problem, report an issue.")


if __name__ == "__main__":
    parser = ArgumentParser("Miled language interpreter")
    parser.add_argument("-f", "--file")
    parser.add_argument("-c", "--code")
    args = parser.parse_args()

    try:
        if args.file is not None:
            file = open(args.file, "r").read()
            try_run(file)
        elif args.code is not None:
            try_run(args.code)
    except FileNotFoundError:
        print("File not found.")
    except Exception as E:
        print("Unknown error occurred:")
        print(E)
