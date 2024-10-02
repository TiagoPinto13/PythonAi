import json
import os
from pythonAI_wrapper.assistant import OpenAIAssistant


class AssistantManager:
    def __init__(self, filename='assistants.json'):
        self.assistants = {}
        self.filename = filename  # Use um nome de arquivo padrão
        self.load_assistants()

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
                        threads=assistant_data.get('threads', {})  # Carrega as threads, se existirem
                    )

    def save_assistants(self):
        """Salva assistentes em um arquivo JSON."""
        data = {
            name: {
                'api_key': assistant.api_key,
                'model': assistant.model,
                'instructions': assistant.instructions,
                'threads': assistant.threads  # Adiciona threads ao salvamento
            } for name, assistant in self.assistants.items()
        }
        with open(self.filename, 'w') as f:
            json.dump(data, f)

    def create_assistant(self, api_key: str, name: str, model: str = 'gpt-4', instructions: str = ''):
        """Cria um novo assistente com o nome fornecido."""
        if name in self.assistants:
            raise ValueError(f"Já existe um assistente com o nome '{name}'.")

        # Criação de um novo assistente
        self.assistants[name] = OpenAIAssistant(api_key=api_key, name=name, model=model, instructions=instructions)

        # Salvar assistentes após a criação
        self.save_assistants()

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
        
        # Salvar assistentes após a criação da thread
        self.save_assistants()  # Salvar as mudanças após criar uma thread
        
        return thread_id

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
        """Envia um prompt para o assistente na thread especificada."""
        if assistant_name not in self.assistants:
            raise ValueError(f"Assistente '{assistant_name}' não encontrado.")
        
        if thread_id not in self.assistants[assistant_name].threads:
            raise ValueError(f"Thread '{thread_id}' não encontrada.")

        # Envia o prompt e obtém a resposta
        response = self.assistants[assistant_name].get_response(prompt)  # Chama o método get_response do assistente
        self.assistants[assistant_name].threads[thread_id].append(response)  # Adiciona a resposta à thread
        self.save_assistants()  # Salva as alterações após enviar o prompt
        return response
