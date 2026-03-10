'''
expression → literal | unary | binary | grouping

literal    → NUMBER | STRING | "true" | "false" | "nil"
grouping   → "(" expression ")"
unary      → ( "-" | "!" ) expression
binary     → expression operator expression
operator   → "==" | "!=" | "<" | "<=" | ">" | ">=" | "+" | "-" | "*" | "/"
'''
'''
Precdeence rules in C:
Lowest to Highest, Unary is the most important one, evaluate first
Name	                    Operators	    Associates
Expression  ->  Equality	 == !=	        Left
Equality    ->  Comparison	 > >= < <=	    Left
Comparsion  ->  Term	     - +	        Left
Term        ->  Factor	     / *	        Left
Factor      ->  Unary	     ! -	        Right
Unary       ->  Primary     NUMBER | STRING | "true" | "false" | "nil" | "(" expression ")" ;

Grammar notation	Code representation
Terminal	        Code to match and consume a token
Nonterminal	        Call to that rule’s function
|	                if or switch statement
* or +	            while or for loop
?	                if statement
'''
# import os
# import sys
# sys.path. append(os.path.join(os.path.dirname(__file__)))
# from get_token_type import * 

class Expr:
    """Base class for all expressions"""
    def accept(self, visitor):
        raise NotImplementedError("Subclass must implement accept()")


class Binary(Expr):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right
    
    def accept(self, visitor):
        return visitor.visitBinaryExpr(self)


class Grouping(Expr):
    def __init__(self, expression):
        self.expression = expression
    
    def accept(self, visitor):
        return visitor.visitGroupingExpr(self)


class Literal(Expr):
    def __init__(self, value):
        self.value = value
    
    def accept(self, visitor):
        return visitor.visitLiteralExpr(self)


class Unary(Expr):
    def __init__(self, operator, right):
        self.operator = operator
        self.right = right
    
    def accept(self, visitor):
        return visitor.visitUnaryExpr(self)


class AstPrinter:
    def print(self, expr: Expr):
        return expr.accept(self)
    
    def visitBinaryExpr(self, expr: Binary):
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)
    
    def visitGroupingExpr(self, expr: Grouping):
        return self.parenthesize("group", expr.expression)
    
    def visitLiteralExpr(self, expr: Literal):
        if expr.value is None:
            return "nil"
        if isinstance(expr.value, bool):
            return "true" if expr.value else "false"  # ✅ Fixed: Python True -> "true"
        if isinstance(expr.value, float):
            # e.g. 2.0 stays "2.0", not "2"
            if expr.value == int(expr.value):
                return f"{int(expr.value)}.0"
            return str(expr.value)
        return str(expr.value)
    
    def visitUnaryExpr(self, expr: Unary):
        return self.parenthesize(expr.operator.lexeme, expr.right)
    
    def parenthesize(self, name: str, *exprs: Expr):
        builder = [name]
        for expr in exprs:
            builder.append(expr.accept(self))
        return f"({' '.join(builder)})"


# ========== TEST CODE ==========

# if __name__ == "__main__": 
#     """
#     Test the AST printer with manually constructed trees.
#     """
    
#     print("=== Testing AstPrinter ===\n")
    
#     # Test 1: Simple literal
#     print("Test 1: Literal 123")
#     expr1 = Literal(123)
#     printer = AstPrinter()
#     result1 = printer.print(expr1)
#     print(f"Result: {result1}")
#     print(f"Expected: 123\n")
    
#     # Test 2: Unary expression:   -123
#     print("Test 2: Unary -123")
#     expr2 = Unary(
#         Token(TokenType.MINUS, "-", None, 1),
#         Literal(123)
#     )
#     result2 = printer.print(expr2)
#     print(f"Result: {result2}")
#     print(f"Expected: (- 123)\n")
    
#     # Test 3: Binary expression:  1 + 2
#     print("Test 3: Binary 1 + 2")
#     expr3 = Binary(
#         Literal(1),
#         Token(TokenType.PLUS, "+", None, 1),
#         Literal(2)
#     )
#     result3 = printer.print(expr3)
#     print(f"Result: {result3}")
#     print(f"Expected: (+ 1 2)\n")
    
#     # Test 4: Grouping:   (1 + 2)
#     print("Test 4: Grouping (1 + 2)")
#     expr4 = Grouping(
#         Binary(
#             Literal(1),
#             Token(TokenType. PLUS, "+", None, 1),
#             Literal(2)
#         )
#     )
#     result4 = printer.print(expr4)
#     print(f"Result: {result4}")
#     print(f"Expected: (group (+ 1 2))\n")
    
#     # Test 5: Complex:   -123 * (45. 67)
#     print("Test 5: Complex -123 * (45.67)")
#     expr5 = Binary(
#         Unary(
#             Token(TokenType. MINUS, "-", None, 1),
#             Literal(123)
#         ),
#         Token(TokenType.STAR, "*", None, 1),
#         Grouping(
#             Literal(45.67)
#         )
#     )
#     result5 = printer.print(expr5)
#     print(f"Result: {result5}")
#     print(f"Expected: (* (- 123) (group 45.67))\n")
    
#     # Test 6: Very complex:  (1 + 2) * (4 - 3)
#     print("Test 6: Very complex (1 + 2) * (4 - 3)")
#     expr6 = Binary(
#         Grouping(
#             Binary(
#                 Literal(1),
#                 Token(TokenType.PLUS, "+", None, 1),
#                 Literal(2)
#             )
#         ),
#         Token(TokenType.STAR, "*", None, 1),
#         Grouping(
#             Binary(
#                 Literal(4),
#                 Token(TokenType.MINUS, "-", None, 1),
#                 Literal(3)
#             )
#         )
#     )
#     result6 = printer.print(expr6)
#     print(f"Result: {result6}")
#     print(f"Expected: (* (group (+ 1 2)) (group (- 4 3)))\n")
    
#     # Test 7: Boolean literals
#     print("Test 7: Boolean ! true")
#     expr7 = Unary(
#         Token(TokenType. BANG, "!", None, 1),
#         Literal(True)
#     )
#     result7 = printer.print(expr7)
#     print(f"Result: {result7}")
#     print(f"Expected: (! True)\n")
    
#     # Test 8: Nil
#     print("Test 8: Nil literal")
#     expr8 = Literal(None)
#     result8 = printer.print(expr8)
#     print(f"Result: {result8}")
#     print(f"Expected: nil\n")
    
#     print("=== All tests complete! ===")