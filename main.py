from lexer import Lexer
from parser import Parser

def main():
    # کد تست شما که قبلاً خطا می‌داد
    code = """
    public sub main ( ) ;
        dim x as integer ;
        readonly y = 10 ;
        x = 5 + y ;
        print "Result is:" ک
        x = [32e2];
        print x ;
    end sub
    """
    
    try:
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        
        parser = Parser(tokens)
        parser.parse_P()
        
    except Exception as e:
        print(f"❌ خطا: {e}")

if __name__ == "__main__":
    main()