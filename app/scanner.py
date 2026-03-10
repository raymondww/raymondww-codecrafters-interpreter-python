import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__)))
from get_token_type import *

class Scanner:
    """
    Scanner class - converts source code (string) into tokens.
    
    Responsibilities:
    - Read through source code character by character
    - Group characters into tokens (lexemes)
    - Identify token types (numbers, strings, operators, keywords)
    - Track line numbers for error reporting
    - Handle lexical errors (invalid characters)
    """
    
    def __init__(self, source:  str, silent: bool=False):
        """
        Initialize the scanner with source code.
        
        Args:
            source:  The entire source code as a string
        
        Attributes:
            start:  Marks the beginning of the current lexeme being scanned
            current: Points to the character currently being examined
            line:  Tracks which line we're on (for error messages)
            source: The source code string
            has_error: Flag to track if any errors occurred
            tokens: List to store all created Token objects
        """
        self.start = 0
        self.current = 0
        self.line = 1
        self.source = source
        self.has_error = False
        self.tokens = []
        self.silent = silent 
        
    def scanToken(self) -> None:
        """
        Scan a single token from the source code. 
        
        This is the heart of the scanner. It:
        1. Gets the next character via advance()
        2. Determines what kind of token it starts
        3. Consumes additional characters if needed (multi-char tokens)
        4. Creates the appropriate token via addToken()
        
        Handles:
        - Whitespace (ignored)
        - Single-character tokens:  ( ) { } , . - + ; * /
        - Two-character tokens: != == <= >= 
        - Comments:  // until end of line
        - String literals: "..."
        - Number literals: 123, 45.67
        - Identifiers and keywords: var, if, myVariable
        - Invalid characters (reports error)
        """
        char = self.advance()
        
        # Ignore whitespace (space, carriage return, tab)
        if char in ' \r\t': 
            return
        
        # Track newlines for line numbers
        if char == '\n': 
            self.line += 1
            return
        
        # Single-character tokens
        if char == '(': 
            self.addToken(TokenType.LEFT_PAREN)
        elif char == ')': 
            self.addToken(TokenType.RIGHT_PAREN)
        elif char == '{': 
            self.addToken(TokenType.LEFT_BRACE)
        elif char == '}': 
            self.addToken(TokenType.RIGHT_BRACE)
        elif char == ',':  
            self.addToken(TokenType.COMMA)
        elif char == '.':  
            self.addToken(TokenType.DOT)
        elif char == '-': 
            self.addToken(TokenType. MINUS)
        elif char == '+':  
            self.addToken(TokenType.PLUS)
        elif char == ';': 
            self.addToken(TokenType.SEMICOLON)
        elif char == '*': 
            self.addToken(TokenType.STAR)
        
        # Slash or comment
        elif char == '/': 
            # Check for comment:  //
            if self.peek() == '/':
                # Comment goes until end of line - consume all characters
                while self.peek() != '\n' and self.current < len(self.source):
                    self.advance()
            else:
                # Just a division operator
                self.addToken(TokenType.SLASH)
        
        # Bang or bang-equal:   !  or !=
        elif char == '!': 
            if self.peek() == '=':
                self.advance()  # Consume the '='
                self.addToken(TokenType.BANG_EQUAL)
            else:
                self.addToken(TokenType.BANG)
        
        # Equal or equal-equal: = or ==
        elif char == '=':  
            if self.peek() == '=':
                self.advance()  # Consume the second '='
                self.addToken(TokenType.EQUAL_EQUAL)
            else:
                self.addToken(TokenType. EQUAL)
        
        # Less or less-equal:   < or <=
        elif char == '<': 
            if self.peek() == '=':
                self.advance()  # Consume the '='
                self.addToken(TokenType. LESS_EQUAL)
            else:
                self.addToken(TokenType.LESS)
        
        # Greater or greater-equal:  > or >=
        elif char == '>':
            if self.peek() == '=':
                self.advance()  # Consume the '='
                self.addToken(TokenType. GREATER_EQUAL)
            else:
                self.addToken(TokenType.GREATER)
        
        # String literal:   "..."
        elif char == '"':
            # Keep scanning until we find the closing "
            while self.peek() != '"' and self.current < len(self.source):
                # Strings can span multiple lines in Lox
                if self.peek() == '\n':
                    self.line += 1
                self.advance()
            
            # Check if we ran out of input (unterminated string)
            if self.current >= len(self. source):
                print(f"[line {self.line}] Error: Unterminated string.", file=sys.stderr)
                self.has_error = True
                return
            
            # Consume the closing "
            self.advance()
            self.addToken(TokenType.STRING)
        
        # Number literal:  123 or 45.67
        elif self.isDigit(char):
            # Consume all digits
            while self.isDigit(self.peek()):
                self.advance()
            
            # Check for decimal part
            if self.peek() == '.' and self.isDigit(self.peek_next()):
                # Consume the '.'
                self.advance()
                
                # Consume fractional digits
                while self.isDigit(self.peek()):
                    self.advance()
            
            self.addToken(TokenType.NUMBER)
        
        # Identifier or keyword:   myVar, if, class, etc.
        elif self.isAlpha(char):
            # Consume all alphanumeric characters
            while self.isAlphaNumeric(self.peek()):
                self.advance()
            
            # addToken will check if it's a keyword
            self.addToken(TokenType. IDENTIFIER)
        
        # Unknown/invalid character
        else: 
            print(f"[line {self. line}] Error: Unexpected character: {char}", file=sys. stderr)
            self.has_error = True
            
    def scanTokens(self) -> None:
        """
        Scan all tokens from the source code.
        
        Main entry point for scanning.  Repeatedly calls scanToken() 
        until we reach the end of the source code, then adds an EOF token.
        
        Process:
        1. Loop through entire source
        2. Mark start of each lexeme
        3. Scan one token
        4. Repeat until end of source
        5. Add EOF token
        """
        while self.current < len(self.source):
            # Mark the start of the next lexeme
            self.start = self.current
            self.scanToken()
        
        # Add EOF token at the end
        eof_token = Token(TokenType.EOF, "", "null", self.line)
        self.tokens.append(eof_token)
        if not self.silent: 
            print(eof_token.toString())
        
    def advance(self) -> str:
        """
        Consume the current character and return it. 
        
        This is like an iterator's next() method - it returns the 
        current character and moves the 'current' pointer forward.
        
        Returns:
            The character at the current position
        """
        char = self.source[self. current]
        self.current += 1
        return char
    
    def peek(self) -> str:
        """
        Look at the current character WITHOUT consuming it.
        
        This is like "lookahead" - we need to see what's coming next
        to decide what token we're building, but we don't consume it yet.
        
        Example:  When we see '! ', we peek ahead to check if it's '! =' or just '!'
        
        Returns: 
            The character at current position, or '\0' if at end
        """
        if self.current >= len(self.source):
            return '\0'  # Null character signals end of input
        return self. source[self.current]
    
    def peek_next(self) -> str:
        """
        Look TWO characters ahead WITHOUT consuming anything.
        
        Needed for number literals to check for decimals.
        Example: "123.456" - when we see '.', we need to check if 
        the next char is a digit to know if it's a decimal or just a dot.
        
        Returns:
            The character one position ahead of current, or '\0' if at/past end
        """
        if self.current + 1 >= len(self.source):
            return '\0'
        return self.source[self. current + 1]
        
    def addToken(self, token_type:  str) -> None:
        """
        Create a token and add it to the tokens list.
        
        Extracts the lexeme from source[start:current] and determines
        the literal value based on token type.
        
        Args:
            token_type: The type of token (NUMBER, STRING, PLUS, etc.)
        
        Process:
        1. Extract lexeme from source code (start to current)
        2. Determine literal value: 
           - STRING: strip quotes
           - NUMBER: convert to float
           - IDENTIFIER: check if it's a keyword
           - Others: use "null"
        3. Create Token object
        4. Add to tokens list
        5. Print token (for Chapter 4 requirement)
        """
        # Extract the text of this token
        lexeme = self. source[self.start:self. current]
        literal = "null"  # Default literal value
        
        if token_type == TokenType.STRING:
            # For strings, strip the surrounding quotes
            # "hello" becomes hello
            literal = lexeme[1:-1]
        
        elif token_type == TokenType.NUMBER:
            # Convert the string to a float
            # "123.45" becomes 123.45
            literal = float(lexeme)
        
        elif token_type == TokenType.IDENTIFIER:
            # Check if this identifier is actually a keyword
            # e.g., "var" should be VAR token, not IDENTIFIER
            if lexeme in TokenType.hash_map:
                token_type = TokenType.hash_map[lexeme]
        
        # Create the token object
        token = Token(token_type, lexeme, literal, self.line)
        
        self.tokens.append(token)
        # print(self.tokens)
        if not self.silent:
            print(token.toString())
        
    def isDigit(self, char: str) -> bool:
        """
        Check if a character is a digit (0-9).
        
        Args:
            char: Single character to check
        
        Returns:
            True if char is '0' through '9', False otherwise
        """
        return char >= '0' and char <= '9'
    
    def isAlpha(self, char: str) -> bool:
        """
        Check if a character is alphabetic or underscore.
        
        In Lox (and most languages), identifiers can start with:
        - Letters:  a-z, A-Z
        - Underscore: _
        
        Args:
            char: Single character to check
        
        Returns:
            True if char is a letter or underscore, False otherwise
        """
        return (char >= 'a' and char <= 'z') or \
               (char >= 'A' and char <= 'Z') or \
               char == '_'
    
    def isAlphaNumeric(self, char: str) -> bool:
        """
        Check if a character is alphanumeric or underscore.
        
        After the first character, identifiers can contain:
        - Letters: a-z, A-Z
        - Digits: 0-9
        - Underscore: _
        
        Examples:  myVar, my_var, myVar123
        
        Args:
            char: Single character to check
        
        Returns:
            True if char is letter, digit, or underscore; False otherwise
        """
        return self.isAlpha(char) or self.isDigit(char)
