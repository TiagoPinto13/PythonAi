import argparse
from pythonAI_wrapper.assistant_manager import AssistantManager
from config import OPENAI_API_KEY
from pythonAI_wrapper.pdfHandler import PDFHandler
import os
def main():
    parser = argparse.ArgumentParser(description="CLI tool for OpenAI Assistant")

    # Definindo os comandos
    subparsers = parser.add_subparsers(dest="command")

    # Comando para criar um assistente
    create_parser = subparsers.add_parser("create_assistant", help="Create a new assistant")
    create_parser.add_argument("name", help="Name of the assistant")
    create_parser.add_argument("--model", default="gpt-4", help="OpenAI model to use")
    create_parser.add_argument("--instructions", help="Instructions for the assistant")

    # Comando para criar uma thread
    create_thread_parser = subparsers.add_parser("create_thread", help="Create a new conversation thread")
    create_thread_parser.add_argument("assistant_name", help="Name of the assistant to use")
    create_thread_parser.add_argument("thread_id", nargs='?', default=None, help="ID of the conversation thread (optional)")

    # Comando para enviar um prompt
    prompt_parser = subparsers.add_parser("send", help="Send a prompt to the assistant")
    prompt_parser.add_argument("assistant_name", help="Name of the assistant to use")
    prompt_parser.add_argument("thread_id", help="ID of the conversation thread")
    prompt_parser.add_argument("prompt", help="Prompt to send")
    
    # Comando para listar assistentes
    list_assistants_parser = subparsers.add_parser("list_assistants", help="List all assistants")

    # Comando para listar threads de um assistente
    list_threads_parser = subparsers.add_parser("list_threads", help="List all threads for an assistant")
    list_threads_parser.add_argument("assistant_name", help="Name of the assistant to list threads")

    # Comando para ver o histórico de uma thread
    history_parser = subparsers.add_parser("history", help="View the history of a thread")
    history_parser.add_argument("assistant_name", help="Name of the assistant")
    history_parser.add_argument("thread_id", help="ID of the conversation thread")
    
    # Comando para ver o histórico de assistentes
    assistant_history_parser = subparsers.add_parser("assistant_history", help="View the history of an assistant")
    assistant_history_parser.add_argument("assistant_name", help="Name of the assistant")

    #  Comando para adicionar um arquivo PDF
    add_file_parser = subparsers.add_parser("add_file", help="Add a PDF file to a thread")
    add_file_parser.add_argument("thread_id", help="ID of the thread")
    add_file_parser.add_argument("file", type=str, help="Path to the PDF file to add")

    # Comando para adicionar uma pasta com arquivos PDF
    add_folder_parser = subparsers.add_parser("add_folder", help="Add all PDF files from a folder to a thread")
    add_folder_parser.add_argument("thread_id", help="ID of the thread")
    add_folder_parser.add_argument("folder", type=str, help="Path to the folder containing PDF files")
    
    # Comando para criar um assistente
    create_parser = subparsers.add_parser("create_assistant", help="Create a new assistant")
    create_parser.add_argument("name", help="Name of the assistant")
    create_parser.add_argument("--model", default="gpt-4", help="OpenAI model to use")
    create_parser.add_argument("--instructions", help="Path to a file or folder with instructions")

    # Comando para enviar um prompt
    prompt_parser = subparsers.add_parser("send", help="Send a prompt to the assistant")
    prompt_parser.add_argument("assistant_name", help="Name of the assistant to use")
    prompt_parser.add_argument("thread_id", help="ID of the conversation thread")
    prompt_parser.add_argument("prompt", help="Path to a text file, folder, or prompt text")

    args = parser.parse_args()

    # Instancia o gerenciador de assistentes
    manager = AssistantManager()

    if args.command == "create_assistant":
        if not OPENAI_API_KEY:
            print("A chave da API não está definida no config.py.")
            return
        
        try:
            manager.create_assistant(OPENAI_API_KEY, args.name, args.model, args.instructions)
            print(f"Assistente '{args.name}' criado com sucesso!")
        except ValueError as e:
            print(e)

    elif args.command == "create_thread":
        if not OPENAI_API_KEY:
            print("A chave da API não está definida no config.py.")
            return
        
        try:
            thread_id = manager.create_thread(args.assistant_name, args.thread_id)
            print(f"Thread '{thread_id}' criada com sucesso usando o assistente '{args.assistant_name}'!")
        except ValueError as e:
            print(e)

    elif args.command == "send":
        try:
            prompt = args.prompt
            
            # Verifique se o argumento é um diretório
            if os.path.isdir(args.prompt):
                files = os.listdir(args.prompt)
                prompt = ""

                if not files:
                    print("A pasta está vazia.")
                    return
                
                # Ler todos os arquivos de texto na pasta
                for file_name in files:
                    file_path = os.path.join(args.prompt, file_name)
                    if file_name.endswith('.pdf'):  
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            prompt += content + "\n"  # Adiciona o conteúdo do arquivo ao prompt
                    else:
                        print(f"Ignorando o arquivo: {file_name} (não é um arquivo .txt)")

                if not prompt.strip():
                    print("Nenhum conteúdo válido encontrado nos arquivos de texto.")
                    return

            response = manager.send_prompt(args.assistant_name, args.thread_id, prompt)
            print(f"Resposta: {response}")
        except Exception as e:
            print(f"Ocorreu um erro: {e}")

    elif args.command == "list_assistants":
        assistants = manager.list_assistants()
        print("Assistentes disponíveis:")
        for assistant in assistants:
            print(assistant)

    elif args.command == "list_threads":
        try:
            threads = manager.list_threads(args.assistant_name)
            print(f"Threads para o assistente '{args.assistant_name}':")
            for thread in threads:
                print(thread)
        except ValueError as e:
            print(e)

    elif args.command == 'history':
        try:
            history = manager.get_thread_history(args.assistant_name, args.thread_id)
            print("Histórico da Thread:")
            for message in history:
                if isinstance(message, dict):
                    role = message.get('role', 'Desconhecido')
                    content = message.get('content', 'Sem conteúdo')
                    role_name = "Usuário" if role == "user" else "Assistente"
                    print(f"{role_name}: {content}")
                else:
                    print(message)  # Caso seja apenas uma string
        except ValueError as e:
            print(e)


    elif args.command == "assistant_history":
        try:
            history = manager.get_assistant_history(args.assistant_name)
            print(f"Histórico do Assistente: {history['assistant_name']}")
            for thread_id, messages in history["threads"].items():
                print(f"\nThread ID: {thread_id}")
                for message in messages:
                    role = message['role']
                    content = message['content']
                    role_name = "Usuário" if role == "user" else "Assistente"
                    print(f"{role_name}: {content}")
        except ValueError as e:
            print(e)


    elif args.command == "add_file":
        try:
            manager.add_context_file(args.file, args.thread_id)
            print(f"Arquivo '{args.file}' adicionado à thread '{args.thread_id}'.")
        except ValueError as e:
            print(e)

    elif args.command == "add_folder":
        try:
            manager.add_context_folder(args.folder, args.thread_id)
            print(f"Todos os arquivos PDF na pasta '{args.folder}' foram adicionados à thread '{args.thread_id}'.")
        except ValueError as e:
            print(e)
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
