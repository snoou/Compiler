from my_token import Token, TokenType

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.line = 1
        self.col = 1

    def advance(self):
        if self.pos < len(self.text):
            ch = self.text[self.pos]
            self.pos += 1
            if ch == '\n':
                self.line += 1
                self.col = 1
            else:
                self.col += 1
            return ch
        return '\0'

    def peek(self):
        return self.text[self.pos] if self.pos < len(self.text) else '\0'

    def tokenize(self):
        tokens = []
        keywords = {
            "dim": TokenType.DIM, "readonly": TokenType.READONLY, "as": TokenType.AS,
            "char": TokenType.CHAR, "integer": TokenType.INTEGER, "boolean": TokenType.BOOLEAN,
            "double": TokenType.DOUBLE, "real": TokenType.REAL, "do": TokenType.DO,
            "while": TokenType.WHILE, "loop": TokenType.LOOP, "for": TokenType.FOR,
            "next": TokenType.NEXT, "to": TokenType.TO, "return": TokenType.RETURN,
            "read": TokenType.READ, "print": TokenType.PRINT, "string": TokenType.STRING,
            "if": TokenType.IF, "then": TokenType.THEN, "else": TokenType.ELSE,
            "endif": TokenType.ENDIF, "end": TokenType.END, "functoin": TokenType.FUNCTOIN,
            "main": TokenType.MAIN, "public": TokenType.PUBLIC, "sub": TokenType.SUB,
            "byref": TokenType.BYREF, "byval": TokenType.BYVAL, "mod": TokenType.MOD
        }

        while self.pos < len(self.text):
            ch = self.peek()
            if ch.isspace():
                self.advance()
            elif ch.isalpha() or ch == '_':
                start_col = self.col
                s = ""
                while self.peek().isalnum() or self.peek() == '_':
                    s += self.advance()
                t_type = keywords.get(s.lower(), TokenType.IDENTIFIER)
                tokens.append(Token(t_type, s, self.line, start_col))
            elif ch.isdigit():
                start_col = self.col
                s = ""
                while self.peek().isdigit():
                    s += self.advance()
                tokens.append(Token(TokenType.NUM_LITERAL, s, self.line, start_col))
            elif ch == '"':
                start_col = self.col
                self.advance() # skip "
                s = ""
                while self.peek() != '"' and self.peek() != '\0':
                    s += self.advance()
                self.advance() # skip "
                tokens.append(Token(TokenType.STRING_LITERAL, s, self.line, start_col))
            else:
                # Operators & Symbols
                start_col = self.col
                if ch == '<':
                    self.advance()
                    if self.peek() == '>': self.advance(); tokens.append(Token(TokenType.NOT_EQUAL, "<>", self.line, start_col))
                    elif self.peek() == '=': self.advance(); tokens.append(Token(TokenType.LESS_EQUAL, "<=", self.line, start_col))
                    else: tokens.append(Token(TokenType.LESS, "<", self.line, start_col))
                elif ch == '>':
                    self.advance()
                    if self.peek() == '=': self.advance(); tokens.append(Token(TokenType.GREATER_EQUAL, ">=", self.line, start_col))
                    else: tokens.append(Token(TokenType.GREATER, ">", self.line, start_col))
                elif ch == '=':
                    self.advance(); tokens.append(Token(TokenType.EQUAL, "=", self.line, start_col))
                else:
                    simple = {'+': TokenType.PLUS, '-': TokenType.MINUS, '*': TokenType.MULTIPLY, '/': TokenType.DIVIDE, 
                              '^': TokenType.POWER, '(': TokenType.LPAREN, ')': TokenType.RPAREN, '[': TokenType.LBRACKET, 
                              ']': TokenType.RBRACKET, ';': TokenType.SEMICOLON, ':': TokenType.COLON, ',': TokenType.COMMA}
                    if ch in simple:
                        tokens.append(Token(simple[ch], ch, self.line, start_col))
                        self.advance()
                    else:
                        self.advance() # Error/Unknown
        tokens.append(Token(TokenType.EOF, "$", self.line, self.col))
        return tokens