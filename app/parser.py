import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__)))
from get_token_type import *
from expr import *

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0  
    
    def parse(self):
        """Main entry point"""
        try:
            return self.expression()
        except Exception as error:
            print(f"Parse error: {error}", file=sys.stderr)
            return None
    
    def expression(self):
        """expression → equality"""
        return self.equality()
    
    def equality(self):
        """equality → comparison ( ( "!=" | "==" ) comparison )*"""
        expr = self.comparison()
        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = Binary(expr, operator, right)
        return expr
    
    def comparison(self):
        """comparison → term ( ( ">" | ">=" | "<" | "<=" ) term )*"""
        expr = self.term()
        while self.match(TokenType.GREATER, TokenType.GREATER_EQUAL,
                         TokenType.LESS, TokenType.LESS_EQUAL):
            operator = self.previous()
            right = self.term()
            expr = Binary(expr, operator, right)
        return expr

    def term(self):
        """term → factor ( ( "-" | "+" ) factor )*"""
        expr = self.factor()
        while self.match(TokenType.MINUS, TokenType.PLUS):
            operator = self.previous()
            right = self.factor()
            expr = Binary(expr, operator, right)  # ✅ Fixed: was Binary(operator, right, expr)
        return expr
    
    def factor(self):
        """factor → unary ( ( "/" | "*" ) unary )*"""
        expr = self.unary()
        while self.match(TokenType.SLASH, TokenType.STAR):
            operator = self.previous()
            right = self.unary()
            expr = Binary(expr, operator, right)  # ✅ Fixed: was Binary(operator, right, expr)
        return expr
    
    def unary(self):
        """unary → ( "!" | "-" ) unary | primary"""
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)  # ✅ Fixed: now returns, doesn't fall through
        return self.primary()              # ✅ Fixed: calls real primary()
        
    def primary(self):
        """primary → NUMBER | STRING | "true" | "false" | "nil" | "(" expression ")" """
        if self.match(TokenType.hash_map['false']):  # 'FALSE'
            return Literal(False)
        if self.match(TokenType.hash_map['true']):   # 'TRUE'
            return Literal(True)
        if self.match(TokenType.hash_map['nil']):    # 'NIL'
            return Literal(None)
        if self.match(TokenType.NUMBER, TokenType.STRING):
            return Literal(self.previous().literal)
        if self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Grouping(expr)
        raise Exception(f"Expect expression, got '{self.peek().lexeme}'")

    # ===== Helper Methods =====
    
    def match(self, *token_types):
        """Check and consume token if it matches"""
        for token_type in token_types:
            if self.check(token_type):
                self.advance()
                return True
        return False
    
    def check(self, token_type):
        """Check token type WITHOUT consuming"""
        if self.isAtEnd():
            return False
        return self.peek().type == token_type
    
    def advance(self):
        """Consume current token"""
        if not self.isAtEnd():
            self.current += 1
        return self.previous()

    def consume(self, token_type, message):
        """Consume token of expected type or raise error"""
        if self.check(token_type):
            return self.advance()
        raise Exception(message)
    
    def isAtEnd(self):
        """Check if at EOF"""
        return self.peek().type == TokenType.EOF
    
    def peek(self):
        """Look at current token"""
        return self.tokens[self.current] 
    
    def previous(self):
        """Get previous token"""
        return self.tokens[self.current - 1]  

# printer = AstPrinter()

# # Test 1: Simple comparison
# print("\n=== Test 1: Simple Comparison ===")
# print("Expression: 1 < 2")
# tokens = [
#     Token(TokenType.NUMBER, "1", 1.0, 1),
#     Token(TokenType.LESS, "<", "null", 1),
#     Token(TokenType.NUMBER, "2", 2.0, 1),
#     Token(TokenType.EOF, "", "null", 1)
# ]
# parser = Parser(tokens)
# tree = parser.parse()
# if tree:
#     result = printer.print(tree)
#     print(f"Result: {result}")
#     print(f"Expected: (< 1.0 2.0)")
#     print("PASS" if result == "(< 1.0 2.0)" else "FAIL")
    
# tokens2 = [
#     Token(TokenType.NUMBER,"1",1.0,1),
#     Token(TokenType.BANG_EQUAL,"==","null",1),
#     Token(TokenType.NUMBER,"1",1.0,1),
#     Token(TokenType.EOF,"","null",1)
# ]
# parser = Parser(tokens2)
# tree = parser.parse()
# if tree:
#     result = printer.print(tree)
#     print(f"Result: {result}")

# 1+1/3
# token3 = [
#     Token(TokenType.NUMBER,"1",1.0,1),
#     Token(TokenType.PLUS,"+","null",1),
#     Token(TokenType.NUMBER,"1",1.0,1),
#     Token(TokenType.SLASH,"/","null",1),
#     Token(TokenType.NUMBER,"3",3.0,1),    
#     Token(TokenType.EOF,"","null",1)
# ]
# parser = Parser(token3)
# tree = parser.parse()
# if tree:
#     result = printer.print(tree)
#     print(f"Result: {result}")