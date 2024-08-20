# parser.py

from symbol_table import SymbolTable

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.symbol_table = SymbolTable()  # Tabela de símbolos para armazenar variáveis
        self.operations = []  # Lista para armazenar operações de atribuição
        self.used_vars = set()  # Conjunto para armazenar variáveis usadas
        self.initialized_vars = set()  # Conjunto para armazenar variáveis inicializadas
        self.next_token()

    def next_token(self):
        self.current_token = self.tokens.pop(0) if self.tokens else None

    def parse(self):
        self.program()
        self.check_unused_variables()

    def program(self):
        if self.current_token[0] == 'PROGRAM':
            self.next_token()
            self.declarations()
            self.block()
            # Ignorar tokens de NEWLINE antes de verificar END
            while self.current_token and self.current_token[0] == 'NEWLINE':
                self.next_token()
            if self.current_token is not None and self.current_token[0] == 'END':
                self.next_token()
            else:
                self.error('END keyword missing')
        else:
            self.error('PROGRAM keyword missing')

    def declarations(self):
        # Ignora NEWLINE antes de DECLARE
        while self.current_token[0] == 'NEWLINE':
            self.next_token()

        if self.current_token[0] == 'DECLARE':
            self.next_token()  # Consome 'declare'

            while True:
                if self.current_token[0] in ('INT_TYPE', 'FLOAT_TYPE', 'STRING_TYPE'):
                    var_type = self.current_token[1]  # Armazena o tipo de variável (int, float ou string)
                    self.next_token()

                    while self.current_token[0] == 'ID':
                        var_name = self.current_token[1]
                        print(f"Processing declaration of {var_name} as {var_type}")
                        self.symbol_table.add_symbol(var_name, var_type)
                        self.operations.append({'type': 'declaration', 'variable': var_name, 'var_type': var_type})  # Adiciona a declaração à lista de operações
                        self.next_token()  # Consome o ID

                        if self.current_token[0] == 'COMMA':
                            self.next_token()  # Consome a vírgula e continua
                        elif self.current_token[0] == 'SEMICOLON':
                            self.next_token()  # Consome o ponto final que encerra as declarações
                            break  # Sai do loop interno e continua com o próximo tipo de variável
                        else:
                            self.error('Expected COMMA or SEMICOLON after variable declaration')

                    if self.current_token[0] == 'SEMICOLON':
                        self.next_token()  # Consome o ponto final que encerra todas as declarações
                        break
                else:
                    break  # Sai do loop se não encontrar mais tipos de variáveis

            if self.current_token[0] != 'NEWLINE':
                self.error('Expected newline or end of declarations')
        else:
            self.error('DECLARE keyword missing')



    def block(self):
        while self.current_token and self.current_token[0] not in ('END', 'RBRACE'):
            if self.current_token[0] == 'ID':
                self.statement()
            elif self.current_token[0] == 'IF':
                self.if_statement()
            elif self.current_token[0] == 'WHILE':
                self.while_statement()
            elif self.current_token[0] == 'DO':
                self.do_while_statement()
            elif self.current_token[0] == 'PRINT':
                self.statement()
            elif self.current_token[0] == 'READ':  # Adicionando reconhecimento para READ
                self.read_statement()
            elif self.current_token[0] == 'NEWLINE':
                self.next_token()
            else:
                self.error(f'Unexpected token in block: {self.current_token}')

    def while_statement(self):
        print(f"Processing WHILE statement, current token: {self.current_token}")
        self.next_token()  # Consome 'WHILE'
        if self.current_token[0] != 'LPAREN':
            self.error('Expected "(" after "enquanto"')
        self.next_token()  # Consome '('
        condition = self.expression()  # Captura a condição
        print(f"While Condition: {condition}")
        if self.current_token[0] == 'RPAREN':
            self.next_token()  # Consome ')'
            if self.current_token[0] == 'LBRACE':  # Verifica a abertura do bloco
                self.next_token()  # Consome '{'
                self.operations.append({'type': 'while_start', 'condition': condition})
                self.block()  # Processa o bloco do while
                if self.current_token[0] == 'RBRACE':
                    self.next_token()  # Consome '}'
                    self.operations.append({'type': 'while_end'})
                else:
                    self.error('Missing closing brace for while block')
            elif self.current_token[0] == 'DO':  # Caso onde há um 'faca' após a condição
                self.next_token()  # Consome 'faca'
                if self.current_token[0] == 'LBRACE':  # Verifica a abertura do bloco após 'faca'
                    self.next_token()  # Consome '{'
                    self.operations.append({'type': 'while_start', 'condition': condition})
                    self.block()  # Processa o bloco do while
                    if self.current_token[0] == 'RBRACE':
                        self.next_token()  # Consome '}'
                        self.operations.append({'type': 'while_end'})
                    else:
                        self.error('Missing closing brace for while block')
                else:
                    self.error('Missing opening brace after "faca"')
            else:
                self.error('Expected "{" or "faca" after while condition')
        else:
            self.error('Missing closing parenthesis in while condition')



    def do_while_statement(self):
        print(f"Processing DO-WHILE statement, current token: {self.current_token}")
        self.next_token()  # Consome 'faca'
        self.operations.append({'type': 'do_while_start'})

        if self.current_token[0] == 'LBRACE':
            self.next_token()  # Consome '{'
            self.block()  # Processa o bloco dentro do DO

            if self.current_token[0] == 'RBRACE':
                self.next_token()  # Consome '}'
                if self.current_token[0] == 'WHILE':  # Verifica se há um WHILE após o DO
                    self.next_token()  # Consome 'enquanto'
                    if self.current_token[0] == 'LPAREN':
                        self.next_token()  # Consome '('
                        condition = self.expression()  # Captura a condição
                        if self.current_token[0] == 'RPAREN':
                            self.next_token()  # Consome ')'
                            if self.current_token[0] == 'SEMICOLON':
                                self.next_token()  # Consome o ';' final
                                self.operations.append({'type': 'do_while_end', 'condition': condition})
                            else:
                                self.error('Missing semicolon after while condition')
                        else:
                            self.error('Missing closing parenthesis in while condition')
                    else:
                        self.error('Missing opening parenthesis after while')
                else:
                    self.error('Expected "enquanto" after "faca" block')
            else:
                self.error('Missing closing brace for do-while block')
        else:
            self.error('Missing opening brace for "faca" block')


    def statement(self):
        if self.current_token[0] == 'ID':
            self.assignment()
        elif self.current_token[0] == 'PRINT':
            self.print_statement()
        elif self.current_token[0] == 'READ':
            self.read_statement()
        elif self.current_token[0] == 'IF':
            self.if_statement()
        elif self.current_token[0] == 'WHILE':
            self.while_statement()
        elif self.current_token[0] == 'DO':  # Adiciona o reconhecimento do comando "faça"
            self.do_while_statement()
        else:
            self.error('Invalid statement')

    def assignment(self):
        print(f"Processing assignment, current token: {self.current_token}")
        var_name = self.current_token[1]  # Armazena o nome da variável
        self.used_vars.add(var_name)  # Marca a variável como usada
        self.next_token()  # Consume ID
        print(f"After ID, current token: {self.current_token}")
        if self.current_token[0] == 'ASSIGN':
            self.next_token()
            expr = self.expression()  # Gera a expressão completa
            self.operations.append({'type': 'assignment', 'variable': var_name, 'value': expr})  # Armazena a operação
            self.initialized_vars.add(var_name)  # Marca a variável como inicializada
            if self.current_token[0] == 'SEMICOLON':
                self.next_token()
            else:
                self.error('Missing semicolon after assignment')
        else:
            self.error('Missing assignment operator')

    def print_statement(self):
        self.next_token()  # Consume PRINT
        if self.current_token[0] == 'LPAREN':
            self.next_token()
            value = self.current_token[1]  # Captura o valor a ser impresso
            if self.current_token[0] == 'ID':
                self.check_initialized(value)  # Verifica se a variável foi inicializada antes de ser usada
            self.operations.append({'type': 'print', 'value': value})
            self.next_token()
            if self.current_token[0] == 'RPAREN':
                self.next_token()
                if self.current_token[0] == 'SEMICOLON':
                    self.next_token()
                else:
                    self.error('Missing semicolon after print')
            else:
                self.error('Missing closing parenthesis')
        else:
            self.error('Missing opening parenthesis')

    def read_statement(self):
        self.next_token()  # Consume READ
        if self.current_token[0] == 'LPAREN':
            self.next_token()
            if self.current_token[0] == 'ID':
                var_name = self.current_token[1]
                self.used_vars.add(var_name)  # Marca a variável como usada
                self.initialized_vars.add(var_name)  # Marca a variável como inicializada
                # Adiciona a operação de leitura à lista de operações
                self.operations.append({'type': 'read', 'variable': var_name})
                self.next_token()
                if self.current_token[0] == 'RPAREN':
                    self.next_token()
                    if self.current_token[0] == 'SEMICOLON':
                        self.next_token()
                    else:
                        self.error('Missing semicolon after read')
                else:
                    self.error('Missing closing parenthesis')
            else:
                self.error('Expected ID in read statement')
        else:
            self.error('Missing opening parenthesis')


    def if_statement(self):
        print(f"Processing IF statement, current token: {self.current_token}")
        self.next_token()  # Consume IF
        print(f"After IF, current token: {self.current_token}")

        if self.current_token[0] != 'LPAREN':
            self.error('Expected "(" after "se"')

        if self.current_token[0] == 'LPAREN':
            self.next_token()
            print(f"After LPAREN, current token: {self.current_token}")

            condition = self.expression()  # Captura a condição
            print(f"Condition: {condition}")

            if self.current_token[0] == 'RPAREN':
                self.next_token()
                print(f"After RPAREN, current token: {self.current_token}")

                if self.current_token[0] == 'THEN':  # Espera o token THEN
                    self.next_token()
                    print(f"After THEN, current token: {self.current_token}")

                    if self.current_token[0] == 'LBRACE':
                        self.next_token()
                        print(f"After LBRACE, current token: {self.current_token}")

                        # Inicia o bloco IF
                        self.operations.append({'type': 'if_start', 'condition': condition})

                        self.block()  # Processa o bloco dentro do IF

                        print(f"After block in IF, current token: {self.current_token}")

                        if self.current_token[0] == 'RBRACE':
                            self.next_token()
                            print(f"After RBRACE in IF, current token: {self.current_token}")

                            if self.current_token[0] == 'ELSE':  # Verifica a presença de um ELSE
                                self.operations.append({'type': 'else_start'})
                                self.next_token()
                                print(f"After ELSE, current token: {self.current_token}")

                                if self.current_token[0] == 'LBRACE':
                                    self.next_token()
                                    print(f"After LBRACE in ELSE, current token: {self.current_token}")

                                    self.block()  # Processa o bloco dentro do ELSE

                                    print(f"After block in ELSE, current token: {self.current_token}")

                                    if self.current_token[0] == 'RBRACE':
                                        self.next_token()
                                        print(f"After RBRACE in ELSE, current token: {self.current_token}")
                                    else:
                                        self.error('Missing closing brace for else block')
                                else:
                                    self.error('Missing opening brace for else block')
                            else:
                                print(f"Unexpected token after IF block: {self.current_token}")
                            self.operations.append({'type': 'if_end'})
                        else:
                            self.error('Missing closing brace for if block')
                    else:
                        self.error('Missing opening brace for if block')
                else:
                    self.error('Missing THEN keyword')
            else:
                self.error('Missing closing parenthesis in if condition')
        else:
            self.error('Missing opening parenthesis in if condition')

    def expression(self):
        # Consome o primeiro operando (deve ser ID, NUMBER ou STRING)
        if self.current_token[0] in ('ID', 'NUMBER', 'STRING'):
            left_operand = self.current_token[1]
            if self.current_token[0] == 'ID':
                self.check_initialized(left_operand)  # Verifica se a variável foi inicializada antes de ser usada
                self.used_vars.add(left_operand)  # Marca a variável como usada
            self.next_token()

            # Agora, verifica se há operadores de comparação ou aritméticos/concatenação
            while self.current_token and self.current_token[0] in ('EQUALS', 'PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE', 'GREATER', 'LESS', 'GREATEREQUAL', 'LESSEQUAL'):
                operator = self.current_token[1]
                self.next_token()
                if self.current_token[0] in ('ID', 'NUMBER', 'STRING'):
                    right_operand = self.current_token[1]
                    if self.current_token[0] == 'ID':
                        self.check_initialized(right_operand)  # Verifica se a variável foi inicializada antes de ser usada
                        self.used_vars.add(right_operand)  # Marca a variável como usada
                    left_operand = f"{left_operand} {operator} {right_operand}"
                    self.next_token()
                else:
                    self.error('Expected ID, NUMBER, or STRING after operator')

            return left_operand
        else:
            self.error('Invalid expression')

    def check_initialized(self, var_name):
        if var_name not in self.initialized_vars:
            self.error(f'Variable "{var_name}" used without being initialized')

    def check_unused_variables(self):
        unused_vars = set(self.symbol_table.symbols.keys()) - self.used_vars
        if unused_vars:
            print(f"Warning: The following variables were declared but never used: {', '.join(unused_vars)}")

    def error(self, message):
        raise Exception(f'Syntax error: {message}')
