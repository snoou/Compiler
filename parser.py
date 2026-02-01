from my_token import TokenType

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current(self): return self.tokens[self.pos]
    
    def eat(self, t_type):
        if self.current().token_type == t_type:
            token = self.current()
            self.pos += 1
            return token
        raise Exception(f"خطای نحوی در خط {self.current().line}: انتظار {t_type.name} داشتیم اما {self.current().token_type.name} پیدا شد.")

    def parse_P(self):
        self.eat(TokenType.PUBLIC)
        self.eat(TokenType.SUB)
        self.eat(TokenType.MAIN)
        self.eat(TokenType.LPAREN)
        self.eat(TokenType.RPAREN)
        self.eat(TokenType.SEMICOLON)
        self.parse_ST()
        self.eat(TokenType.SEMICOLON) # این سمی‌کالنِ قبل از End Sub است
        self.eat(TokenType.END)
        self.eat(TokenType.SUB)
        print("✅ برنامه با موفقیت تحلیل شد و هیچ خطای نحوی ندارد.")

    def parse_ST(self):
        self.parse_Stmt()
        self.parse_ZZ()

    def parse_ZZ(self):
        # اگر توکن فعلی سمی‌کالن است، چک می‌کنیم آیا بعد از آن دستور دیگری هست یا خیر
        if self.current().token_type == TokenType.SEMICOLON:
            # نگاه به توکن بعدی بدون مصرف کردن آن
            next_t = self.tokens[self.pos + 1].token_type if self.pos + 1 < len(self.tokens) else None
            # لیست توکن‌هایی که می‌توانند شروع‌کننده یک دستور جدید باشند
            stmt_starts = [TokenType.IDENTIFIER, TokenType.IF, TokenType.DO, TokenType.FOR, 
                           TokenType.PRINT, TokenType.READ, TokenType.DIM, TokenType.READONLY, 
                           TokenType.SUB, TokenType.FUNCTOIN]
            
            if next_t in stmt_starts:
                self.eat(TokenType.SEMICOLON) # مصرف سمی‌کالن به عنوان جداکننده
                self.parse_ST()
        # در غیر این صورت، قانون اپسیلون اجرا می‌شود و به متد قبلی برمی‌گردد

    def parse_Stmt(self):
        cur = self.current().token_type
        if cur == TokenType.IDENTIFIER: self.parse_Assign()
        elif cur in [TokenType.DO, TokenType.FOR]: self.parse_OO()
        elif cur == TokenType.IF: self.parse_IF()
        elif cur == TokenType.FUNCTOIN: self.parse_Func()
        elif cur == TokenType.PRINT: self.parse_PRINT()
        elif cur == TokenType.READ: self.parse_READ()
        elif cur == TokenType.SUB: self.parse_EE()
        elif cur in [TokenType.DIM, TokenType.READONLY]: self.parse_VV()
        else: raise Exception(f"دستور نامعتبر در خط {self.current().line}")

    def parse_VV(self):
        if self.current().token_type == TokenType.DIM:
            self.eat(TokenType.DIM); self.eat(TokenType.IDENTIFIER); self.parse_YY()
        else:
            self.eat(TokenType.READONLY); self.eat(TokenType.IDENTIFIER); self.parse_CC()

    def parse_YY(self):
        if self.current().token_type == TokenType.LBRACKET:
            self.eat(TokenType.LBRACKET); self.parse_Term(); self.eat(TokenType.RBRACKET); self.parse_BB()
        else: self.parse_AA()

    def parse_AA(self):
        if self.current().token_type == TokenType.COMMA:
            self.eat(TokenType.COMMA); self.eat(TokenType.IDENTIFIER); self.parse_AA()
        else: self.eat(TokenType.AS); self.parse_Type()

    def parse_BB(self):
        if self.current().token_type == TokenType.COMMA:
            self.eat(TokenType.COMMA); self.eat(TokenType.IDENTIFIER)
            self.eat(TokenType.LBRACKET); self.parse_Term(); self.eat(TokenType.RBRACKET); self.parse_BB()
        else: self.eat(TokenType.AS); self.parse_Type()

    def parse_CC(self):
        if self.current().token_type == TokenType.COMMA:
            self.eat(TokenType.COMMA); self.eat(TokenType.IDENTIFIER); self.parse_CC()
        else: self.eat(TokenType.EQUAL); self.parse_Term()

    def parse_Assign(self):
        self.eat(TokenType.IDENTIFIER)
        if self.current().token_type == TokenType.LBRACKET:
            self.eat(TokenType.LBRACKET); self.parse_Term(); self.eat(TokenType.RBRACKET)
        self.eat(TokenType.EQUAL)
        if self.current().token_type == TokenType.STRING_LITERAL: self.eat(TokenType.STRING_LITERAL)
        else: self.parse_Term()

    def parse_IF(self):
        self.eat(TokenType.IF); self.parse_Term(); self.parse_Relop(); self.parse_Term()
        self.eat(TokenType.THEN); self.eat(TokenType.SEMICOLON); self.parse_ST()
        self.eat(TokenType.SEMICOLON); self.eat(TokenType.ELSE); self.eat(TokenType.SEMICOLON)
        self.parse_ST(); self.eat(TokenType.SEMICOLON); self.eat(TokenType.ENDIF)

    def parse_OO(self):
        if self.current().token_type == TokenType.DO:
            self.eat(TokenType.DO); self.eat(TokenType.WHILE); self.parse_Term(); self.parse_Relop(); self.parse_Term()
            self.eat(TokenType.SEMICOLON); self.parse_ST(); self.eat(TokenType.SEMICOLON); self.eat(TokenType.LOOP)
        else:
            self.eat(TokenType.FOR); self.eat(TokenType.IDENTIFIER); self.eat(TokenType.EQUAL); self.parse_Term()
            self.eat(TokenType.TO); self.parse_Term(); self.eat(TokenType.SEMICOLON)
            self.parse_ST(); self.eat(TokenType.SEMICOLON); self.eat(TokenType.NEXT)

    def parse_PRINT(self):
        self.eat(TokenType.PRINT)
        if self.current().token_type == TokenType.STRING_LITERAL: self.eat(TokenType.STRING_LITERAL)
        else: self.parse_Term()

    def parse_READ(self):
        self.eat(TokenType.READ); self.eat(TokenType.IDENTIFIER)
        if self.current().token_type == TokenType.LBRACKET:
            self.eat(TokenType.LBRACKET); self.parse_Term(); self.eat(TokenType.RBRACKET)

    def parse_Func(self):
        self.eat(TokenType.FUNCTOIN); self.eat(TokenType.IDENTIFIER); self.eat(TokenType.LPAREN)
        self.parse_param(); self.eat(TokenType.RPAREN); self.eat(TokenType.COLON); self.eat(TokenType.AS)
        self.parse_Type(); self.eat(TokenType.SEMICOLON); self.parse_ST(); self.eat(TokenType.SEMICOLON)
        self.eat(TokenType.RETURN); self.parse_Term(); self.eat(TokenType.SEMICOLON); self.eat(TokenType.END); self.eat(TokenType.FUNCTOIN)

    def parse_EE(self):
        self.eat(TokenType.SUB); self.eat(TokenType.IDENTIFIER); self.eat(TokenType.LPAREN)
        self.parse_param(); self.eat(TokenType.RPAREN); self.eat(TokenType.SEMICOLON)
        self.parse_ST(); self.eat(TokenType.SEMICOLON); self.eat(TokenType.END); self.eat(TokenType.SUB)

    def parse_Type(self):
        types = [TokenType.CHAR, TokenType.INTEGER, TokenType.BOOLEAN, TokenType.DOUBLE, TokenType.REAL, TokenType.STRING]
        if self.current().token_type in types: self.pos += 1
        else: raise Exception("نوع داده نامعتبر")

    def parse_Relop(self):
        ops = [TokenType.LESS_EQUAL, TokenType.GREATER_EQUAL, TokenType.NOT_EQUAL, TokenType.EQUAL, TokenType.GREATER, TokenType.LESS]
        if self.current().token_type in ops: self.pos += 1
        else: raise Exception("عملگر مقایسه‌ای نامعتبر")

    def parse_param(self):
        if self.current().token_type in [TokenType.BYVAL, TokenType.BYREF]:
            self.pos += 1; self.eat(TokenType.IDENTIFIER); self.eat(TokenType.AS); self.parse_Type()
            if self.current().token_type == TokenType.COMMA: self.eat(TokenType.COMMA); self.parse_param()

    def parse_Term(self):
        if self.current().token_type in [TokenType.PLUS, TokenType.MINUS]: self.pos += 1
        self.parse_EXP()

    def parse_EXP(self):
        self.parse_T()
        while self.current().token_type in [TokenType.PLUS, TokenType.MINUS]:
            self.pos += 1; self.parse_T()

    def parse_T(self):
        self.parse_F()
        while self.current().token_type in [TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MOD]:
            self.pos += 1; self.parse_F()

    def parse_F(self):
        self.parse_I()
        if self.current().token_type == TokenType.POWER: self.eat(TokenType.POWER); self.parse_F()

    def parse_I(self):
        cur = self.current().token_type
        if cur == TokenType.IDENTIFIER: self.eat(TokenType.IDENTIFIER)
        elif cur == TokenType.NUM_LITERAL: self.eat(TokenType.NUM_LITERAL)
        elif cur == TokenType.LPAREN: self.eat(TokenType.LPAREN); self.parse_EXP(); self.eat(TokenType.RPAREN)
        else: raise Exception("انتظار عدد یا شناسه")