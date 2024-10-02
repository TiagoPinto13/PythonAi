# PythonAi

PythonAI é uma ferramenta de linha de comando (CLI) que permite interagir com um assistente OpenAI. Você pode criar assistentes, gerenciar threads de conversa e adicionar contexto a essas interações.

## Requisitos

- Python 3.x
- Certifique-se de ter as bibliotecas necessárias instaladas, usando `pip install -r requirements.txt`.

## Configuração

Antes de usar a CLI, defina a chave da API do OpenAI no arquivo `config.py`:

```python
# config.py

OPENAI_API_KEY = 'sua_chave_api_aqui'
```
## Commands to use CLI Tool:

### Criar um Assistente:
  * python3 cli_tool.py create_assistant <nome_do_assistente> [--model <modelo>] [--instructions <instruções>]
    
    * <nome_do_assistente>: Nome do assistente a ser criado.
    * model: Modelo da OpenAI a ser utilizado (padrão: gpt-4).
    * instructions: Instruções personalizadas para o assistente.

### Criar uma Nova Thread de Conversa:
  * python3 cli_tool.py create_thread <nome_do_assistente> [<id_da_thread>]
    
      * <nome_do_assistente>: Nome do assistente a ser utilizado.
      * <id_da_thread>: ID da thread (opcional).
### Enviar um Prompt:
  * python3 cli_tool.py send <nome_do_assistente> <id_da_thread> <prompt>
  
    * <nome_do_assistente>: Nome do assistente a ser utilizado.
    * <id_da_thread>: ID da thread.
    * <prompt>: O prompt a ser enviado ao assistente.

### Listar Assistentes:
  * python3 cli_tool.py list_assistants

### Listar Threads de um Assistente:
  * python3 cli_tool.py list_threads <nome_do_assistente>
  
    * <nome_do_assistente>: Nome do assistente para listar suas threads.

### Ver Histórico de uma Thread:
  * python3 cli_tool.py history <nome_do_assistente> <id_da_thread>

    * <nome_do_assistente>: Nome do assistente.
    * <id_da_thread>: ID da thread para ver o histórico.




