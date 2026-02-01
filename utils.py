def is_letter_or_underscore(ch: str) -> bool:
    return ch.isalpha() or ch == "_"

def is_digit(ch: str) -> bool:
    return ch.isdigit()

def is_whitespace_char(ch: str) -> bool:
    return ch in [" ", "\t", "\n", "\r"]

def is_keyword(word: str) -> bool:
    keywords = [
        "dim", "readonly", "as", "char", "integer", "boolean", "double",
        "real", "do", "while", "loop", "for", "next", "to", "return",
        "read", "print", "string", "if", "then", "else", "endif", "end",
        "functoin", "main", "public", "sub", "byref", "byval", "mod"
    ]
    return word.lower() in keywords