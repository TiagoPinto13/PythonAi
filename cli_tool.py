import argparse
from pythonAI_wrapper.assistant_manager import AssistantManager
from config import OPENAI_API_KEY

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
            # Aqui é onde corrigimos a chamada do método
            response = manager.send_prompt(args.assistant_name, args.thread_id, args.prompt)
            print(f"Resposta: {response}")
        except ValueError as e:
            print(e)

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

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
