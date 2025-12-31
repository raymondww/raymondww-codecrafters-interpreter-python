import sys
from get_token_type import TokenType

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
SLASH = TokenType()['SLASH']
EOF = TokenType()['EOF']
BANG = TokenType()['BANG']
BANG_EQUAL = TokenType()['BANG_EQUAL']
EQUAL = TokenType()['EQUAL']
EQUAL_EQUAL = TokenType()['EQUAL_EQUAL']
GREATER = TokenType()['GREATER']
GREATER_EQUAL = TokenType()['GREATER_EQUAL']
LESS = TokenType()['LESS']
LESS_EQUAL = TokenType()['LESS_EQUAL']
STRING = TokenType()['STRING']
NUMBER = TokenType()['NUMBER']
IDENTIFIER = TokenType()['IDENTIFIER']
hash_map = TokenType()['hash_map']
    
class Scanner:
    def __init__(self, source:str):
        self.start = 0
        self.current = 0
        self.line = 1
        self.source = source
        self.has_error = False
        
    def scanToken(self)->None:
        char = self.advance()  
        # Ignore whitespace
        if char in ' \r\t':
            return
        # read new line
        if char == '\n':
            self.line += 1
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
        elif char == '/':
            if self.peek() == '/':
                # A comment goes until the end of the line.
                while self.peek() != '\n' and self.current < len(self.source):
                    self.advance()
            else: self.addToken(SLASH)
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
        elif char == '"':
            # string literal, keep scanning until we find the ending "
            while self.peek() != '"' and self.current < len(self.source):
                if self.peek() == '\n':
                    self.line += 1
                self.advance()
            if self.current >= len(self.source):
                print(f"[line {self.line}] Error: Unterminated string.", file=sys.stderr)
                self.has_error = True
                return
            # The closing ".
            self.advance()
            self.addToken(STRING)
        elif self.isDigit(char):
            while self.isDigit(self.peek()) and self.current < len(self.source):
                self.advance()
            if self.peek() == '.' and self.isDigit(self.peek_next()):
                self.advance()
                while self.isDigit(self.peek()) and self.current < len(self.source):
                    self.advance()
            self.addToken(NUMBER)
        elif self.isAlpha(char):
            while self.isAlphaNumeric(self.peek()) and self.current < len(self.source):
                self.advance()
            self.addToken(IDENTIFIER)
            
        else: 
            # Unknown character - report error to stderr
            print(f"[line {self.line}] Error: Unexpected character: {char}", file=sys.stderr)
            self.has_error = True
            
    def scanTokens(self)->None:
        while self.current < len(self.source):
            self.start = self.current
            self.scanToken()
        print(f"{EOF}  null")
        
    def advance(self)->str:
        """Get current character and move forward"""
        char = self.source[self.current]
        self.current += 1
        return char
    
    def peek(self)->str:
        # we call peek() inside scanToken after advance()
        """Look at current character WITHOUT consuming it"""
        if self.current >= len(self.source):
            return '\0'
        return self.source[self.current]
    
    def peek_next(self)->str:
        """Look at next character WITHOUT consuming it"""
        if self.current+1 >= len(self.source):
            return '\0'
        return self.source[self.current+1]
        
    def addToken(self, token_type:str)->None:
        lexeme = self.source[self.start:self.current]
        if token_type == STRING:
            # For STRING tokens, we need to strip the surrounding quotes
            lexeme_strip = lexeme[1:-1]
            print(f"{token_type} {lexeme} {lexeme_strip}")
        elif token_type == NUMBER:
            lexeme_float = float(lexeme)
            print(f"{token_type} {lexeme} {lexeme_float}")
        elif token_type == IDENTIFIER:
            if hash_map.get(lexeme):
                print(f"{token_type} {lexeme} {hash_map.get(lexeme)}")
            else: print(f"{token_type} {lexeme} null")
        else: print(f"{token_type} {lexeme} null")
        
    def isDigit(self,char:str)->bool:
        return char >= '0' and char <= '9'
    
    def isAlpha(self,char:str)->bool:
        return (char >= 'a' and char <= 'z') or (char >= 'A' and char <= 'Z') or char == '_'
    
    def isAlphaNumeric(self,char:str)->bool:
        # logical or to check if the char is a character or number
        # both are valid identifier
        return self.isAlpha(char) or self.isDigit(char)        
        
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
    # print([f for f in file_contents])  # --- IGNORE ---
    scanner = Scanner(file_contents)
    scanner.scanTokens()

    # Exit with code 65 if there were errors
    if scanner.has_error:
        exit(65)


if __name__ == "__main__":
    main()