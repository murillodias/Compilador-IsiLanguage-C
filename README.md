# Integrantes

Nome: Ana Julia Monici Orbetelli - RA: 11201810144

Nome: Murillo Rodrigues Dias - RA: 11201723076

Nome: Vinicius Sedrim - RA: 11201912418

# Projeto Compilador - Documentação

Este projeto é um compilador simples que processa um código de linguagem fictícia e gera um código C correspondente. O projeto é composto por vários módulos que juntos realizam as tarefas de análise léxica, análise sintática, análise semântica, e geração de código.

# Link Apresentação - YouTube

[https://www.youtube.com/watch?v=_zaBHN0V7-c](https://www.youtube.com/watch?v=_zaBHN0V7-c)

## Arquivos do Projeto

### 1. `code_generator.py`

O arquivo `code_generator.py` é responsável por gerar o código C a partir das operações capturadas pelo parser. Este módulo trabalha em conjunto com o parser para transformar a árvore de análise sintática em código executável na linguagem C.

- **Funções principais:**
  - **`generate_program()`**: Inicializa o código C com as inclusões necessárias, como `stdio.h` e `string.h`, e define a função `main`.
  - **`generate_end()`**: Finaliza o código C, adicionando a instrução `return 0;` e fechando a função `main`.
  - **`generate_declaration()`**: Gera declarações de variáveis, cuidando de variáveis do tipo `string` para que sejam tratadas como arrays de `char` no código C.
  - **`generate_assignment()`**: Gera atribuições, tratando especialmente a concatenação de strings.
  - **`generate_print()`**: Gera as instruções `printf` para exibir variáveis ou mensagens.
  - **`generate_read()`**: Gera as instruções `scanf` para leitura de variáveis do usuário.
  - **`generate_if`, `generate_else`, `generate_end_if`**: Geram a estrutura de controle `if-else`.
  - **`generate_while`, `generate_end_while`, `generate_do_while`**: Geram as estruturas de repetição `while` e `do-while`.

### 2. `lexer.py`

O arquivo `lexer.py` implementa o analisador léxico, ou seja, o componente que transforma a entrada de código-fonte em uma sequência de tokens. Cada token é uma unidade atômica de significado, como uma palavra-chave, um identificador, ou um símbolo.

- **Definição dos tokens**: O arquivo define uma lista de padrões de expressão regular para cada tipo de token esperado, como palavras-chave (`programa`, `declare`, `fimprog`), operadores (`+`, `-`, `*`, `/`), tipos de dados (`int`, `float`, `string`), e outros símbolos de linguagem.
- **Função `tokenize()`**: Esta função percorre o código-fonte e, utilizando as expressões regulares definidas, identifica e classifica cada token, construindo uma lista de tokens que será passada para o parser.

### 3. `main.py`

O arquivo `main.py` é o ponto de entrada do compilador. Ele coordena a execução das etapas do processo de compilação: análise léxica, análise sintática, análise semântica (caso implementada), e geração de código.

- **Função `main()`**: Esta função principal recebe o nome do arquivo de código-fonte a ser compilado, executa o lexer para tokenizar o código, o parser para construir a árvore sintática e, finalmente, chama o gerador de código para produzir o código C.
- **Execução**: A função também cuida da criação e escrita do código gerado em um arquivo de saída na pasta `output`.

### 4. `parser.py`

O arquivo `parser.py` contém o analisador sintático, ou parser, responsável por verificar a estrutura gramatical do código-fonte. O parser utiliza os tokens produzidos pelo lexer para construir a árvore de análise sintática e verificar se a estrutura do código está correta.

- **Função `parse()`**: Inicia o processo de análise sintática, começando pela identificação do início do programa e passando pelas declarações de variáveis e blocos de código.
- **Função `declarations()`**: Processa as declarações de variáveis, verificando os tipos e garantindo que as variáveis sejam declaradas corretamente antes de seu uso.
- **Função `block()`**: Processa os blocos de código, incluindo instruções de controle de fluxo (`if-else`, `while`, `do-while`), atribuições, e operações de entrada/saída.
- **Função `expression()`**: Avalia expressões aritméticas e lógicas, garantindo que sejam válidas conforme as regras da linguagem.

### 5. `semantic.py`

O arquivo `semantic.py` (separado para possível expansão futura) seria responsável por realizar a análise semântica, que verifica a validade dos significados das construções do código, como o uso correto dos tipos de dados, verificação de variáveis não inicializadas, e outras regras que vão além da mera sintaxe.

- **Função de análise semântica**: Este módulo poderia incluir verificações como garantir que uma variável seja inicializada antes do uso, verificar se as operações entre tipos de dados são válidas, entre outras verificações semânticas.

### 6. `symbol_table.py`

O arquivo `symbol_table.py` implementa a tabela de símbolos, uma estrutura fundamental para acompanhar as declarações de variáveis e seus atributos (tipo, valor, escopo, etc.) durante a compilação.

- **Classe `SymbolTable`**: Esta classe gerencia a inserção, atualização e consulta de variáveis na tabela de símbolos.
- **Métodos principais**:
  - **`add_symbol()`**: Adiciona uma nova variável à tabela, juntamente com seu tipo.
  - **`get_type()`**: Retorna o tipo de uma variável, permitindo ao parser e ao analisador semântico realizar verificações de tipo.
  - **`check_symbol()`**: Verifica se uma variável já foi declarada, ajudando a detectar erros como uso de variáveis não declaradas.


## Como Executar

### Pré-requisitos
- **Python 3.x**: Certifique-se de ter o Python 3.x instalado no seu sistema.
- **Compilador C**: Para compilar e executar o código C gerado, você precisará de um compilador C como GCC.

### Passos para Execução
1. **Clonar o Repositório**: Clone este repositório em seu ambiente local.
   ```bash
   git clone https://github.com/Ana-Monici/Compilador-IsiLanguage-C.git
   cd Compilador-IsiLanguage-C

2. **Executar o Compilador**: Execute o compilador apontando para o arquivo .isi dentro da pasta examples.
    ```bash
    python src/main.py examples/arquivo.isi

3. **Verificar o Código C Gerado**: O código C será gerado na pasta output com o mesmo nome do arquivo .isi, mas com extensão .c.

4. **Compilar o Código C**: Compile o código C gerado usando um compilador C, como o GCC.
    ```bash
    gcc output/seu_arquivo.c -o seu_programa

5. **Exemplo Completo**
    ```bash
    python src/main.py examples/example9_two_variable_types.isi
    gcc output/example9_two_variable_types.c -o example9
    ./example9
