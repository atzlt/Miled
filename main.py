import sys

from interpreter.interpret import Interpreter
from argparse import ArgumentParser

if __name__ == "__main__":
    parser = ArgumentParser("Miled language interpreter")
    parser.add_argument("-f", "--file")
    parser.add_argument("-c", "--code")
    args = parser.parse_args()

    try:
        if args.file is not None:
            file = open(args.file, "r").read()
            print(Interpreter(file).run())
        elif args.code is not None:
            print(Interpreter(args.code).run())
    except FileNotFoundError:
        print("File not found.")
    except IndexError:
        print("An IndexError occurred. It's likely that you've used an index out of range, or you have too many "
              "enclosing marks. Check your code.")
    except TypeError:
        print("A TypeError occurred. It's likely that you've forgot to enclose a Caller, or you messed "
              "up the types. Use \"->...\" commands to convert types.")
    except Exception as E:
        print("An error occurred.")
        print(E)
