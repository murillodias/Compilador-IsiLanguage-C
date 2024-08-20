# symbol_table.py

print("SymbolTable module loaded")

class SymbolTable:
    def __init__(self):
        # Inicializa a tabela de símbolos como um dicionário vazio
        self.symbols = {}

    def add_symbol(self, name, var_type, value=None):
        # Adiciona um símbolo à tabela com um nome, tipo e valor opcional
        if name in self.symbols:
            raise Exception(f"Symbol '{name}' already declared.")
        self.symbols[name] = {'type': var_type, 'value': value}

    def get_symbol(self, name):
        # Retorna o tipo e o valor do símbolo se ele existir na tabela
        if name not in self.symbols:
            raise Exception(f"Symbol '{name}' not found.")
        return self.symbols[name]
    
    def set_symbol(self, name, value):
        # Atualiza o valor de um símbolo existente
        if name not in self.symbols:
            raise Exception(f"Symbol '{name}' not found.")
        self.symbols[name]['value'] = value

    def get_symbol_type(self, name):
        # Retorna o tipo da variável
        if name not in self.symbols:
            raise Exception(f"Symbol '{name}' not found.")
        return self.symbols[name]['type']

    def __str__(self):
        # Retorna a tabela de símbolos como uma string
        return str(self.symbols)

# Exemplo de uso
if __name__ == "__main__":
    table = SymbolTable()
    table.add_symbol("a", 10)
    print(table.get_symbol("a"))  # Deve imprimir 10
    table.set_symbol("a", 20)
    print(table.get_symbol("a"))  # Deve imprimir 20
    print(table)
