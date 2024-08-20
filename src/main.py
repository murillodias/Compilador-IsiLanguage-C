# main.py

import os
import sys
from lexer import tokenize
from parser import Parser
from code_generator import CodeGenerator

def main(input_filename):
    with open(input_filename, "r") as file:
        code = file.read()
    
    # Tokenização
    tokens = tokenize(code)
    print("Tokens:", tokens)
    
    # Parsing
    parser = Parser(tokens)
    parser.parse()
    
    # Geração de Código
    generator = CodeGenerator()
    generator.generate_program()
    generator.generate_from_operations(parser.operations)  # Gerar código a partir das operações do parser
    generator.generate_end()
    
    # Saída do código gerado
    generated_code = generator.get_code()
    print(generated_code)
    
    # Salvar o código gerado em um arquivo
    output_filename = os.path.splitext(os.path.basename(input_filename))[0] + ".c"
    output_file_path = os.path.join("output", output_filename)
    
    os.makedirs("output", exist_ok=True)
    with open(output_file_path, "w") as output_file:
        output_file.write(generated_code)
    
    print(f"Código gerado salvo em: {output_file_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <source_file>")
    else:
        main(sys.argv[1])
