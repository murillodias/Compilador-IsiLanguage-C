# semantic.py

class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def declare(self, name):
        if name in self.symbols:
            raise Exception(f'Semantic error: Variable "{name}" already declared')
        self.symbols[name] = None

    def assign(self, name, value):
        if name not in self.symbols:
            raise Exception(f'Semantic error: Variable "{name}" not declared')
        self.symbols[name] = value

    def check(self, name):
        if name not in self.symbols:
            raise Exception(f'Semantic error: Variable "{name}" not declared')
        if self.symbols[name] is None:
            raise Exception(f'Semantic error: Variable "{name}" used without being initialized')

# Exemplo de uso
if __name__ == "__main__":
    symbol_table = SymbolTable()
    symbol_table.declare("a")
    symbol_table.assign("a", 10)
    symbol_table.check("a")
    print("Semantic checks completed successfully!")
