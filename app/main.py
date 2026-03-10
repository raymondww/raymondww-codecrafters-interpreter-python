import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__)))
from scanner import Scanner
from parser import Parser
from get_token_type import *
from expr import *

def main():
    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh tokenize <filename>", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    if command not in ("tokenize", "parse"):
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)

    with open(filename) as file:
        file_contents = file.read()

    if command == "tokenize":
        scanner = Scanner(file_contents)
        scanner.scanTokens()
        if scanner.has_error:
            exit(65)

    elif command == "parse":
        # Scan silently (no printing)
        scanner = Scanner(file_contents, silent=True)
        scanner.scanTokens()
        if scanner.has_error:
            exit(65)
        
        parser = Parser(scanner.tokens)
        ast = parser.parse()
        if ast is None:
            exit(65)
        
        print(AstPrinter().print(ast))


if __name__ == "__main__":
    main()