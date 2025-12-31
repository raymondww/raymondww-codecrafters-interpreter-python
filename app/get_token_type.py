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
    SLASH = 'SLASH' 
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
    hash_map = {'and': 'AND', 'class': 'CLASS', 'else': 'ELSE', 'false': 'FALSE',
                'for': 'FOR', 'fun': 'FUN', 'if': 'IF', 'nil': 'NIL', 'or': 'OR',
                'print': 'PRINT', 'return': 'RETURN', 'super': 'SUPER',
                'this': 'THIS', 'true': 'TRUE', 'var': 'VAR', 'while': 'WHILE'}
    EOF = 'EOF'
    return locals()