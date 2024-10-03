# assistant_manager.py

import json
import os
from pythonAI_wrapper.assistant import OpenAIAssistant
from pythonAI_wrapper.pdfHandler import PDFHandler


class AssistantManager:
    def __init__(self, filename='assistants.json', threads_filename='threads.json'):
        self.assistants = {}
        self.filename = filename  
        self.threads_filename = threads_filename  
        self.load_assistants()
        self.load_threads()  

    def load_assistants(self):
        """Carrega assistentes de um arquivo JSON."""
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                data = json.load(f)
                for name, assistant_data in data.items():
                    self.assistants[name] = OpenAIAssistant(
                        api_key=assistant_data['api_key'],
                        name=name,
                        model=assistant_data['model'],
                        instructions=assistant_data['instructions'],
                    )

    def save_assistants(self):
        """Salva assistentes em um arquivo JSON."""
        data = {
            name: {
                'api_key': assistant.api_key,
                'model': assistant.model,
                'instructions': assistant.instructions,
            } for name, assistant in self.assistants.items()
        }
        with open(self.filename, 'w') as f:
            json.dump(data, f, indent=4)
            
    def get_assistant_history(self, assistant_name):
        """Retorna o histórico das threads de um assistente específico."""
        if assistant_name not in self.assistants:
            raise ValueError(f"Assistente '{assistant_name}' não encontrado.")

        assistant = self.assistants[assistant_name]
        history = {
            "assistant_name": assistant.name,
            "threads": {}
        }

        for thread_id, messages in assistant.threads.items():
            history["threads"][thread_id] = messages

        return history

    def create_assistant(self, api_key: str, name: str, model: str = 'gpt-4', instructions: str = ''):
        """Cria um novo assistente com o nome fornecido e carrega instruções de um arquivo ou pasta."""
        if name in self.assistants:
            raise ValueError(f"Já existe um assistente com o nome '{name}'.")

        # Se instructions é um caminho, leia o conteúdo
        if os.path.isdir(instructions):
            instructions = self.load_instructions_from_folder(instructions)
        elif os.path.isfile(instructions):
            with open(instructions, 'r') as f:
                instructions = f.read()

        # Criação de um novo assistente
        self.assistants[name] = OpenAIAssistant(api_key=api_key, name=name, model=model, instructions=instructions)

        # Salvar assistentes após a criação
        self.save_assistants()

    def load_threads(self):
        """Carrega threads de um arquivo JSON."""
        if os.path.exists(self.threads_filename):
            with open(self.threads_filename, 'r') as f:
                data = json.load(f)
                for assistant_name, threads in data.items():
                    if assistant_name in self.assistants:
                        self.assistants[assistant_name].threads = threads

    def save_threads(self):
        """Salva threads em um arquivo JSON."""
        data = {
            name: assistant.threads for name, assistant in self.assistants.items()
        }
        with open(self.threads_filename, 'w') as f:
            json.dump(data, f, indent=4)

    # As outras funções permanecem as mesmas...
    def create_thread(self, assistant_name: str, thread_id: str = None):
        """Cria uma nova thread para o assistente especificado."""
        if assistant_name not in self.assistants:
            raise ValueError(f"Assistente '{assistant_name}' não encontrado.")

        if thread_id is None:
            thread_id = f"thread_{len(self.assistants[assistant_name].threads) + 1}"

        if thread_id in self.assistants[assistant_name].threads:
            raise ValueError(f"Já existe uma thread com o ID '{thread_id}'.")

        # Criação da nova thread
        self.assistants[assistant_name].threads[thread_id] = []  # Inicializa a thread como uma lista vazia
        
        # Salvar assistentes e threads após a criação da thread
        self.save_assistants()
        self.save_threads()  # Salvar as mudanças após criar uma thread
        
        return thread_id
    
    def get_thread_history(self, assistant_name: str, thread_id: str):
        """
        Retorna o histórico da thread de um assistente específico.
        
        Args:
            assistant_name (str): O nome do assistente.
            thread_id (str): O ID da thread a ser usada.
        
        Returns:
            List[Dict]: O histórico da thread.
        """
        if assistant_name not in self.assistants:
            raise ValueError(f"Assistente '{assistant_name}' não encontrado.")
        
        if thread_id in self.assistants[assistant_name].threads:
            return self.assistants[assistant_name].threads[thread_id]
        else:
            raise ValueError(f"Thread {thread_id} não encontrada.")


    def list_assistants(self):
        """Lista todos os assistentes e seus modelos."""
        return [(name, assistant.model) for name, assistant in self.assistants.items()]

    def list_threads(self, assistant_name):
        """Lista todas as threads do assistente especificado."""
        if assistant_name not in self.assistants:
            raise ValueError(f"Assistente '{assistant_name}' não encontrado.")
        
        return list(self.assistants[assistant_name].threads.keys())  # Corrigido para acessar threads como atributo

    def get_assistant(self, assistant_name):
        """Obtém o assistente especificado pelo nome."""
        if assistant_name not in self.assistants:
            raise ValueError(f"Assistente '{assistant_name}' não encontrado.")
        
        return self.assistants[assistant_name]

    def send_prompt(self, assistant_name, thread_id, prompt):
        """Envia um prompt para o assistente na thread especificada e atualiza o histórico."""
        if assistant_name not in self.assistants:
            raise ValueError(f"Assistente '{assistant_name}' não encontrado.")
        
        assistant = self.assistants[assistant_name]

        # Envia o prompt e obtém a resposta, incluindo o histórico completo na requisição
        response = assistant.get_response(prompt, thread_id)

        # Salva as alterações após enviar o prompt
        self.save_assistants()
        self.save_threads()

        return response
    def add_context_file(self, file_path, thread_id):
        """Adiciona o conteúdo de um arquivo PDF à thread especificada."""
        pdf_handler = PDFHandler()
        pdf_content = pdf_handler.read_pdf(file_path)

        if pdf_content:
            self.add_to_thread(thread_id, pdf_content)  # Certifique-se de que `add_to_thread` existe
            print(f"Conteúdo do arquivo PDF adicionado à thread '{thread_id}'.")
        else:
            print("Erro: Nenhum conteúdo encontrado no PDF.")




    
            
    def load_instructions_from_folder(self, folder_path: str):
        """Lê todos os arquivos de texto em uma pasta e retorna seu conteúdo combinado."""
        instructions = ""
        for file in os.listdir(folder_path):
            if file.endswith('.txt'):
                with open(os.path.join(folder_path, file), 'r') as f:
                    instructions += f.read() + "\n"  # Adiciona o conteúdo do arquivo
        return instructions
    
    def load_prompts_from_folder(self, folder_path: str):
        """Lê todos os arquivos de texto em uma pasta e retorna seu conteúdo combinado."""
        prompts = ""
        for file in os.listdir(folder_path):
            if file.endswith('.txt'):
                with open(os.path.join(folder_path, file), 'r') as f:
                    prompts += f.read() + "\n"  # Adiciona o conteúdo do arquivo
        return prompts
