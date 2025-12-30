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
BANG = TokenType()['BANG']
BANG_EQUAL = TokenType()['BANG_EQUAL']
EQUAL = TokenType()['EQUAL']
EQUAL_EQUAL = TokenType()['EQUAL_EQUAL']
GREATER = TokenType()['GREATER']
GREATER_EQUAL = TokenType()['GREATER_EQUAL']
LESS = TokenType()['LESS']
LESS_EQUAL = TokenType()['LESS_EQUAL']
    
class Scanner:
    def __init__(self, source:str):
        self.start = 0
        self.current = 0
        self.line = 1
        self.source = source
        self.has_error = False
        
    def scanToken(self):
        char = self.advance()        
        # Ignore whitespace
        if char in ' \r\t\n':
            return
        
        # Single-character tokens
        if char == '(': 
            self.addToken(LEFT_PAREN)
        elif char == ')': 
            self.addToken(RIGHT_PAREN)
        elif char == '{': 
            self.addToken(LEFT_BRACE)
        elif char == '}': 
            self.addToken(RIGHT_BRACE)
        elif char == ',':  
            self.addToken(COMMA)
        elif char == '.':  
            self.addToken(DOT)
        elif char == '-': 
            self.addToken(MINUS)
        elif char == '+':  
            self.addToken(PLUS)
        elif char == ';': 
            self.addToken(SEMICOLON)
        elif char == '*': 
            self.addToken(STAR)
        elif char == '!': 
            if self.peek() == '=':
                self.advance()
                self.addToken(BANG_EQUAL)
            else: self.addToken(BANG)
        elif char == '=': 
            if self.peek() == '=':
                self.advance()
                self.addToken(EQUAL_EQUAL)
            else: self.addToken(EQUAL)
        elif char == '<': 
            if self.peek() == '=':
                self.advance()
                self.addToken(LESS_EQUAL)
            else: self.addToken(LESS)
        elif char == '>':
            if self.peek() == '=':
                self.advance()
                self.addToken(GREATER_EQUAL)
            else: self.addToken(GREATER)
        else: 
            # Unknown character - report error to stderr
            print(f"[line 1] Error: Unexpected character: {char}", file=sys.stderr)
            self.has_error = True
            
    def scanTokens(self):
        while self.current < len(self.source):
            self.start = self.current
            self.scanToken()
        print(f"{EOF}  null")
        
    def advance(self):
        """Get current character and move forward"""
        char = self.source[self.current]
        self.current += 1
        return char
    
    def peek(self):
        """Look at current character WITHOUT consuming it"""
        if self.current >= len(self.source):
            return '\0'
        return self.source[self.current]
    
    def addToken(self, token_type):
        lexeme = self.source[self.start:self.current]
        print(f"{token_type} {lexeme} null")
        

def main():    
    if len(sys.argv) < 3:
        print("Usage:  ./your_program.sh tokenize <filename>", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    if command != "tokenize": 
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)

    with open(filename) as file:
        file_contents = file.read()
        
    scanner = Scanner(file_contents)
    scanner.scanTokens()

    # Exit with code 65 if there were errors
    if scanner.has_error:
        exit(65)


if __name__ == "__main__":
    main()