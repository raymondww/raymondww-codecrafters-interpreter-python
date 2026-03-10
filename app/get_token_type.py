class TokenType:
    """
    TokenType class - defines all possible token types in Lox.
    
    Token types are organized into categories:
    - Single-character tokens: ( ) { } , . - + ; * /
    - One or two character tokens: !  != = == < <= > >=
    - Literals:  IDENTIFIER, STRING, NUMBER
    - Keywords: var, if, while, class, etc.
    - EOF:  end of file marker
    """
    
    # Single-character tokens
    # These are operators and delimiters that are always one character
    LEFT_PAREN = 'LEFT_PAREN'      # (
    RIGHT_PAREN = 'RIGHT_PAREN'    # )
    LEFT_BRACE = 'LEFT_BRACE'      # {
    RIGHT_BRACE = 'RIGHT_BRACE'    # }
    COMMA = 'COMMA'                # ,
    DOT = 'DOT'                    # .
    MINUS = 'MINUS'                # -
    PLUS = 'PLUS'                  # +
    SEMICOLON = 'SEMICOLON'        # ;
    STAR = 'STAR'                  # *
    SLASH = 'SLASH'                # /
    
    # One or two character tokens
    # These can be single character OR combined with '=' for comparison
    BANG = 'BANG'                  # !
    BANG_EQUAL = 'BANG_EQUAL'      # !=
    EQUAL = 'EQUAL'                # =
    EQUAL_EQUAL = 'EQUAL_EQUAL'    # ==
    GREATER = 'GREATER'            # >
    GREATER_EQUAL = 'GREATER_EQUAL'  # >=
    LESS = 'LESS'                  # <
    LESS_EQUAL = 'LESS_EQUAL'      # <=
    
    # Literals
    # These represent actual values in the source code
    IDENTIFIER = 'IDENTIFIER'      # Variable names:  myVar, x, _temp
    STRING = 'STRING'              # String literals: "hello"
    NUMBER = 'NUMBER'              # Number literals: 123, 45.67
    
    # Keywords
    # Reserved words in Lox that have special meaning
    # Maps from the keyword text to its token type
    hash_map = {
        'and': 'AND',          # Logical AND operator
        'class': 'CLASS',      # Class declaration
        'else':  'ELSE',        # Else clause
        'false': 'FALSE',      # Boolean false literal
        'for': 'FOR',          # For loop
        'fun': 'FUN',          # Function declaration
        'if': 'IF',            # If statement
        'nil': 'NIL',          # Nil/null literal
        'or': 'OR',            # Logical OR operator
        'print': 'PRINT',      # Print statement
        'return': 'RETURN',    # Return statement
        'super': 'SUPER',      # Superclass reference
        'this':  'THIS',        # Current instance reference
        'true': 'TRUE',        # Boolean true literal
        'var': 'VAR',          # Variable declaration
        'while': 'WHILE'       # While loop
    }
    
    # End of file marker
    EOF = 'EOF'                    # Marks end of source code


class Token:
    """
    Token class - represents a single token from the source code.
    
    A token is a meaningful unit of code (like a word in a sentence).
    Each token has: 
    - type: what kind of token it is (NUMBER, PLUS, IDENTIFIER, etc.)
    - lexeme: the actual text from source code ("123", "+", "myVar")
    - literal: the interpreted value (123. 0, "hello", null)
    - line: which line it appeared on (for error messages)
    
    Example:
        Source code: var x = 123;
        Tokens: 
            Token(VAR, "var", null, 1)
            Token(IDENTIFIER, "x", null, 1)
            Token(EQUAL, "=", null, 1)
            Token(NUMBER, "123", 123.0, 1)
            Token(SEMICOLON, ";", null, 1)
    """
    
    def __init__(self, type, lexeme:  str, literal, line: int):
        """
        Create a new token.
        
        Args:
            type: Token type (from TokenType class)
            lexeme: The raw text from source code
            literal: The interpreted value: 
                     - For numbers: the float value (123.0)
                     - For strings: the string without quotes ("hello")
                     - For others: "null"
            line:  Line number where this token appears
        """
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line
    
    def toString(self):
        """
        Convert token to string representation.
        
        Format:  "TYPE lexeme literal"
        Examples:
            "NUMBER 123 123.0"
            "STRING \"hello\" hello"
            "PLUS + null"
        
        Returns:
            String representation of the token
        """
        # Handle different literal types
        if isinstance(self.literal, str):
            # String or "null"
            return f"{self.type} {self.lexeme} {self. literal}"
        
        elif isinstance(self.literal, float):
            # Number - format with . 0 if whole number
            if self.literal == int(self.literal):
                # 123.0 displays as "123.0" (not "123")
                return f"{self.type} {self.lexeme} {int(self.literal)}.0"
            else:
                # 123.45 displays as "123.45"
                return f"{self.type} {self.lexeme} {self.literal}"
        
        else:
            # Fallback:  convert whatever it is to string
            return f"{self.type} {self.lexeme} {str(self.literal)}"