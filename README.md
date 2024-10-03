# PythonAi

PythonAI é uma ferramenta de linha de comando (CLI) que permite interagir com um assistente OpenAI. Você pode criar assistentes, gerenciar threads de conversa e adicionar contexto a essas interações.

## Requisitos

- Python 3.x
- Certifique-se de ter as bibliotecas necessárias instaladas, usando `pip install -r requirements.txt`.

## Snippet
*  Antes de usar a library, deve alterar a api key com o método change_api_key ou altera-la diretamente no ficheiro config.py

# CLI Tool for OpenAI Assistant
## Comandos Disponíveis


### create_assistant
Cria um novo assistente.

**Uso:**
```
python3 cli_tool.py create_assistant <nome> [--model <modelo>] [--instructions <instruções>]
```

**Argumentos:**
- `<nome>`: Nome do assistente.
- `--model`: (Opcional) Modelo da OpenAI a ser utilizado (default: "gpt-4").
- `--instructions`: (Opcional) Instruções para o assistente.


### create_thread
Cria uma nova thread de conversa.

**Uso:**
```
python3 cli_tool.py create_thread <nome_assistente> [<thread_id>]
```

**Argumentos:**
- `<nome_assistente>`: Nome do assistente a ser utilizado.
- `<thread_id>`: (Opcional) ID da thread de conversa.


### send
Envia um prompt para o assistente.

**Uso:**
```
python3 cli_tool.py send <nome_assistente> <thread_id> <prompt>
```

**Argumentos:**
- `<nome_assistente>`: Nome do assistente a ser utilizado.
- `<thread_id>`: ID da thread de conversa.
- `<prompt>`: Texto ou caminho para um arquivo de texto ou pasta contendo o prompt.

### list_assistants
Lista todos os assistentes disponíveis.

**Uso:**
```
python3 cli_tool.py list_assistants
```


### list_threads
Lista todas as threads de um assistente.

**Uso:**
```
python3 cli_tool.py list_threads <nome_assistente>
```

**Argumentos:**
- `<nome_assistente>`: Nome do assistente cujas threads devem ser listadas.


### history
Visualiza o histórico de uma thread.

**Uso:**
```
python3 cli_tool.py history <nome_assistente> <thread_id>
```

**Argumentos:**
- `<nome_assistente>`: Nome do assistente.
- `<thread_id>`: ID da thread de conversa.


### assistant_history
Visualiza o histórico de um assistente.

**Uso:**
```
python3 cli_tool.py assistant_history <nome_assistente>
```

**Argumentos:**
- `<nome_assistente>`: Nome do assistente.


### Add file as a prompt
Envia um ficheiro para prompt
```
python3 cli_tool.py send <nome_assistente> <thread_id> <caminho_ficheiro>
```
**Argumentos:**
- `<nome_assistente>`: Nome do assistente.
- `<thread_id>`: ID da thread de conversa.
- `<caminho_pasta>`: Caminho para o ficheiro PDF


### Add folder as a prompt
Envia uma pasta para prompt
```
python3 cli_tool.py send <nome_assistente> <thread_id> <caminho_pasta>
```
**Argumentos:**
- `<nome_assistente>`: Nome do assistente.
- `<thread_id>`: ID da thread de conversa.
- `<caminho_pasta>`: Caminho para a pasta contendo arquivos PDF


