# code_generator.py

class CodeGenerator:
    def __init__(self):
        self.output_code = ""
        self.indent_level = 0  # Nível de indentação
        self.declared_variables = {}  # Mantém um registro das variáveis já declaradas e seus tipos

    def increase_indent(self):
        self.indent_level += 1

    def decrease_indent(self):
        self.indent_level -= 1

    def add_line(self, line):
        # Adiciona uma linha com a indentação correta
        self.output_code += "    " * self.indent_level + line + "\n"

    def generate_program(self):
        self.add_line("#include <stdio.h>")
        self.add_line("#include <string.h>")  # Para suportar operações com strings
        self.add_line("int main() {")
        self.increase_indent()

    def generate_end(self):
        self.decrease_indent()
        self.add_line("return 0;")
        self.add_line("}")

    def generate_declaration(self, variable, var_type="int"):
        if variable not in self.declared_variables:
            if var_type == "string":
                # Declarar strings como arrays de char
                self.add_line(f"char {variable}[100];")  # Ajuste o tamanho conforme necessário
            else:
                self.add_line(f"{var_type} {variable};")
            self.declared_variables[variable] = var_type

    def generate_assignment(self, variable, value):
        var_type = self.declared_variables.get(variable, "int")
        
        if var_type == "string":
            # Se o valor contiver strings e operadores de adição, trata como concatenação de strings
            if '+' in value:
                value_parts = value.split('+')
                concat_code = f'strcpy({variable}, {value_parts[0].strip()});'
                for part in value_parts[1:]:
                    concat_code += f' strcat({variable}, {part.strip()});'
                self.add_line(concat_code)
            else:
                # Para uma atribuição simples de string
                self.add_line(f'strcpy({variable}, {value});')
        else:
            if var_type == "float" and "." in value:
                value = f"{value}f"  # Adiciona 'f' aos valores float se necessário
            self.add_line(f"{variable} = {value};")

    def generate_print(self, value):
        if value.startswith('"') and value.endswith('"'):
            self.add_line(f'printf("%s\\n", {value});')
        else:
            var_type = self.declared_variables.get(value, "int")
            if var_type == "float":
                self.add_line(f'printf("%f\\n", {value});')
            elif var_type == "string":
                self.add_line(f'printf("%s\\n", {value});')
            else:
                self.add_line(f'printf("%d\\n", {value});')

    def generate_read(self, variable):
        var_type = self.declared_variables.get(variable, "int")
        if var_type == "float":
            self.add_line(f'scanf("%f", &{variable});')
        elif var_type == "string":
            self.add_line(f'scanf("%s", {variable});')
        else:
            self.add_line(f'scanf("%d", &{variable});')


    def generate_if(self, condition):
        self.add_line(f"if ({condition}) {{")
        self.increase_indent()

    def generate_else(self):
        self.decrease_indent()
        self.add_line("} else {")
        self.increase_indent()

    def generate_end_if(self):
        self.decrease_indent()
        self.add_line("}")

    def generate_while(self, condition):
        self.add_line(f"while ({condition}) {{")
        self.increase_indent()

    def generate_do_while(self, condition):
        self.decrease_indent()
        self.add_line(f"}} while ({condition});")

    def generate_end_while(self):
        self.decrease_indent()
        self.add_line("}")

    def generate_from_operations(self, operations):
        # Primeiro, geramos as declarações de variáveis
        declarations = [op for op in operations if op['type'] == 'declaration']
        for operation in declarations:
            self.generate_declaration(operation['variable'], operation.get('var_type', 'int'))

        # Depois, geramos o restante das operações
        for operation in operations:
            if operation['type'] == 'assignment':
                self.generate_assignment(operation['variable'], operation['value'])
            elif operation['type'] == 'print':
                self.generate_print(operation['value'])
            elif operation['type'] == 'read':  # Certifique-se de que esta linha está presente
                self.generate_read(operation['variable'])
            elif operation['type'] == 'if_start':
                self.generate_if(operation['condition'])
            elif operation['type'] == 'else_start':
                self.generate_else()
            elif operation['type'] == 'if_end':
                self.generate_end_if()
            elif operation['type'] == 'while_start':
                self.generate_while(operation['condition'])
            elif operation['type'] == 'while_end':
                self.generate_end_while()
            elif operation['type'] == 'do_while_start':
                self.add_line("do {")
                self.increase_indent()  # Inicia o bloco do-while
            elif operation['type'] == 'do_while_end':
                self.generate_do_while(operation['condition'])  # Fecha o bloco do-while


    def get_code(self):
        return self.output_code