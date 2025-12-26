import sys

def TokenType():
    # Single-character tokens.
    LEFT_PAREN = 'LEFT_PAREN'
    RIGHT_PAREN = 'RIGHT_PAREN'
    LEFT_BRACE = 'LEFT_BRACE'
    RIGHT_BRACE = 'RIGHT_BRACE'
    COMMA = 'COMMA'
    DOT = 'DOT'
    MINUS = 'MINUS'
    PLUS = 'PLUS'
    SEMICOLON = 'SEMICOLON'
    STAR = 'STAR'
    # one or two character tokens.
    BANG = 'BANG'
    BANG_EQUAL = 'BANG_EQUAL'
    EQUAL = 'EQUAL'
    EQUAL_EQUAL = 'EQUAL_EQUAL'
    GREATER = 'GREATER'
    GREATER_EQUAL = 'GREATER_EQUAL'
    LESS = 'LESS'
    LESS_EQUAL = 'LESS_EQUAL'
    # Literals.
    IDENTIFIER = 'IDENTIFIER'
    STRING = 'STRING'
    NUMBER = 'NUMBER'
    # Keywords.
    AND = 'AND'
    CLASS = 'CLASS'
    ELSE = 'ELSE'
    FALSE = 'FALSE'
    FUN = 'FUN'
    FOR = 'FOR'
    IF = 'IF'
    NIL = 'NIL'
    OR = 'OR'
    PRINT = 'PRINT'
    RETURN = 'RETURN'
    SUPER = 'SUPER'
    THIS = 'THIS'
    TRUE = 'TRUE'
    VAR = 'VAR'
    WHILE = 'WHILE'
    EOF = 'EOF'
    return locals()

LEFT_PAREN = TokenType()['LEFT_PAREN']
RIGHT_PAREN = TokenType()['RIGHT_PAREN']
LEFT_BRACE = TokenType()['LEFT_BRACE']
RIGHT_BRACE = TokenType()['RIGHT_BRACE']
COMMA = TokenType()['COMMA']
DOT = TokenType()['DOT']
MINUS = TokenType()['MINUS']
PLUS = TokenType()['PLUS']
SEMICOLON = TokenType()['SEMICOLON']
STAR = TokenType()['STAR']
EOF = TokenType()['EOF']

def scanToken(char):
    if char=='(': addToken(LEFT_PAREN,char)
    if char==')': addToken(RIGHT_PAREN,char)
    if char=='{': addToken(LEFT_BRACE,char)
    if char=='}': addToken(RIGHT_BRACE,char)
    if char==',': addToken(COMMA,char)
    if char=='.': addToken(DOT,char)
    if char=='-': addToken(MINUS,char)
    if char=='+': addToken(PLUS,char)
    if char==';': addToken(SEMICOLON,char)
    if char=='*': addToken(STAR,char)
    
def addToken(tokenType, lexeme=None):
    text = "null"
    print(f"{tokenType} {lexeme} {text}")

def main():
    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh tokenize <filename>", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    if command != "tokenize":
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)

    with open(filename) as file:
        file_contents = file.read()

    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!", file=sys.stderr)

    if file_contents:
        for char in file_contents:
            scanToken(char)
        print(f"{EOF}  null")
        # raise NotImplementedError("Scanner not implemented")
    else:
        print(f"{EOF}  null") # Placeholder, replace this line when implementing the scanner


if __name__ == "__main__":
    main()
