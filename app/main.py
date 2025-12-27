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

has_error = False

def scanToken(char):
    global has_error
    
    # Ignore whitespace
    if char in ' \r\t\n':
        return
    
    # Single-character tokens
    if char == '(': 
        addToken(LEFT_PAREN, char)
    elif char == ')': 
        addToken(RIGHT_PAREN, char)
    elif char == '{': 
        addToken(LEFT_BRACE, char)
    elif char == '}': 
        addToken(RIGHT_BRACE, char)
    elif char == ',':  
        addToken(COMMA, char)
    elif char == '.':  
        addToken(DOT, char)
    elif char == '-': 
        addToken(MINUS, char)
    elif char == '+':  
        addToken(PLUS, char)
    elif char == ';': 
        addToken(SEMICOLON, char)
    elif char == '*': 
        addToken(STAR, char)
    else: 
        # Unknown character - report error to stderr
        print(f"[line 1] Error: Unexpected character: {char}", file=sys.stderr)
        has_error = True

def addToken(tokenType, lexeme, literal="null"):
    # Print token to stdout
    print(f"{tokenType} {lexeme} {literal}")
def main():
    global has_error
    
    if len(sys.argv) < 3:
        print("Usage:  ./your_program.sh tokenize <filename>", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    filename = sys. argv[2]

    if command != "tokenize": 
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)

    with open(filename) as file:
        file_contents = file.read()

    # Scan all characters
    for char in file_contents: 
        scanToken(char)
    
    # Always print EOF token
    print(f"{EOF}  null")
    
    # Exit with code 65 if there were errors
    if has_error:
        exit(65)


if __name__ == "__main__":
    main()