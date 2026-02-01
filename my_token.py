from enum import Enum, auto
from dataclasses import dataclass
from typing import Union

class TokenType(Enum):
    # Keywords
    DIM = auto(); READONLY = auto(); AS = auto(); CHAR = auto(); INTEGER = auto()
    BOOLEAN = auto(); DOUBLE = auto(); REAL = auto(); DO = auto(); WHILE = auto()
    LOOP = auto(); FOR = auto(); NEXT = auto(); TO = auto(); RETURN = auto()
    READ = auto(); PRINT = auto(); STRING = auto(); IF = auto(); THEN = auto()
    ELSE = auto(); ENDIF = auto(); END = auto(); FUNCTOIN = auto()
    MAIN = auto(); PUBLIC = auto(); SUB = auto(); BYREF = auto(); BYVAL = auto(); MOD = auto()

    # Operators
    PLUS = auto(); MINUS = auto(); MULTIPLY = auto(); DIVIDE = auto(); POWER = auto()
    EQUAL = auto(); NOT_EQUAL = auto(); LESS = auto(); GREATER = auto()
    LESS_EQUAL = auto(); GREATER_EQUAL = auto(); ASSIGN = auto()
    
    # Symbols
    LPAREN = auto(); RPAREN = auto(); LBRACKET = auto(); RBRACKET = auto()
    SEMICOLON = auto(); COMMA = auto(); COLON = auto(); DOT = auto()

    # Literals
    IDENTIFIER = auto(); NUM_LITERAL = auto(); STRING_LITERAL = auto()
    EOF = auto(); ERROR = auto()

@dataclass
class Token:
    token_type: TokenType
    lexeme: str
    line: int
    column: int