# lexer.py
import re

# Definição dos tokens
TOKENS = [
    ('PROGRAM', r'programa'),
    ('END', r'fimprog'),
    ('DECLARE', r'declare'),
    ('PRINT', r'escreva'),
    ('THEN', r'entao'),  # Adicionando o token THEN
    ('READ', r'leia'),
    ('ELSE', r'senao'),  # ELSE deve vir antes de IF
    ('IF', r'se'),  # IF deve vir depois de ELSE
    ('WHILE', r'enquanto'),  # Adicionando suporte para while
    ('DO', r'faca'),  # Adicionando suporte para do while
    ('FLOAT_TYPE', r'float'),  # Token específico para float
    ('INT_TYPE', r'int'),  # Token específico para int
    ('STRING_TYPE', r'string'),  # Token específico para string
    ('ID', r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ('NUMBER', r'\d+(\.\d+)?'),  # Modificado para suportar floats
    ('PLUS', r'\+'),
    ('MINUS', r'\-'),
    ('MULTIPLY', r'\*'),
    ('DIVIDE', r'\/'),
    ('ASSIGN', r':='),
    ('EQUALS', r'=='),
    ('LPAREN', r'\('),
    ('RPAREN', r'\)'),
    ('LBRACE', r'\{'),
    ('RBRACE', r'\}'),
    ('COMMA', r','),  # Adicionando o token COMMA
    ('SEMICOLON', r'\.'),
    ('STRING', r'\".*?\"'),
    ('NEWLINE', r'\n'),
    ('SKIP', r'[ \t]+'),
    ('GREATER', r'>'),
    ('LESS', r'<'),
    ('GREATEREQUAL', r'>='),
    ('LESSEQUAL', r'<='),
    ('NOTEQUAL', r'!='),
    ('MISMATCH', r'.')
]

def tokenize(code):
    tokens = []
    while code:
        match = None
        for token_type, token_pattern in TOKENS:
            regex = re.compile(token_pattern)
            match = regex.match(code)
            if match:
                text = match.group(0)
                if token_type != 'SKIP' and token_type != 'MISMATCH':
                    tokens.append((token_type, text))
                code = code[len(text):]
                break
        if not match:
            raise SyntaxError(f'Unexpected character: {code[0]}')
    return tokens

# Exemplo de uso
if __name__ == "__main__":
    code = '''programa
    declare int a, float b, c.
    a := 10.
    b := 20.5.
    c := a + b.
    escreva("Resultado:").
    escreva(c).
    fimprog
    '''
    tokens = tokenize(code)
    for token in tokens:
        print(token)