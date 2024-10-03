# assistant.py

import os
from typing import List, Dict
from openai import OpenAI
from openai import OpenAI


class OpenAIAssistant:
    def __init__(self, api_key: str, name: str, model: str = 'gpt-4', instructions: str = '', threads=None):
        """
        Inicializa o assistente OpenAI com a chave API, nome, modelo e instruções iniciais.

        Args:
            api_key (str): A chave API da OpenAI para autenticação.
            name (str): O nome do assistente.
            model (str, optional): O modelo de linguagem a ser usado. Padrão é 'gpt-4'.
            instructions (str, optional): Instruções iniciais para o assistente. Padrão é uma string vazia.
            threads (dict, optional): Dicionário de threads associadas ao assistente.
        """
        self.api_key = api_key
        self.client = OpenAI(api_key= self.api_key)

        self.name = name
        self.model = model
        self.instructions = instructions
        self.context_files: List[str] = []
        self.threads: Dict[str, List[Dict]] = threads if threads is not None else {}  # Inicializa threads, se não houver

        # Inicializa o cliente da API OpenAI

    def get_response(self, prompt: str, thread_id: str):
        """Obtém uma resposta do assistente e atualiza o histórico da thread."""
        if thread_id not in self.threads:
            raise ValueError(f"Thread '{thread_id}' não encontrada.")

        # Adiciona a pergunta do usuário ao histórico da thread
        self.threads[thread_id].append({"role": "user", "content": prompt})

        # Chamada à API para obter a resposta do assistente
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.instructions},
                *self.threads[thread_id]  # Envia o histórico completo como contexto
            ]
        )

        assistant_response = response.choices[0].message.content

        # Adiciona a resposta do assistente ao histórico da thread
        self.threads[thread_id].append({"role": "assistant", "content": assistant_response})

        return assistant_response


    def set_model(self, model: str):
        """
        Define o modelo a ser utilizado, tanto localmente quanto no OpenAI.
        
        Args:
            model (str): O modelo de linguagem a ser usado.
        
        Raises:
            ValueError: Se o modelo fornecido não é suportado.
        """
        self.model = model

    def add_context_file(self, file_path, thread_id):
        thread_dir = os.path.join("thread_files", thread_id)
        os.makedirs(thread_dir, exist_ok=True)

        # Obter o nome do arquivo a partir do caminho original
        file_name = os.path.basename(file_path)

        # Criar o novo caminho do arquivo no diretório da thread
        new_file_path = os.path.join(thread_dir, file_name)

        # Copiar o arquivo para o diretório da thread
        with open(file_path, "rb") as source_file:
            with open(new_file_path, "wb") as dest_file:
                dest_file.write(source_file.read())

        # Adiciona o arquivo ao sistema
        file_object = self.client.files.create(
            file=open(new_file_path, "rb"),
            purpose="assistants"
        )

        # Adicionar o arquivo à thread
        self.client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content="",
            file_ids=[file_object.id]
        )

        return file_object.id


    def add_context_folder(self, folder_path: str, thread_id: str):
        """
        Adiciona todos os arquivos PDF de uma pasta.

        Args:
            folder_path (str): O caminho para a pasta a ser adicionada.
            thread_id (str): O ID da thread a ser usado para adicionar arquivos.
        
        Raises:
            NotADirectoryError: Se o caminho fornecido não é um diretório.
        """
        if not os.path.isdir(folder_path):
            raise NotADirectoryError(f"{folder_path} não é um diretório.")

        for file in os.listdir(folder_path):
            if file.endswith('.pdf'):
                # Chama o método add_context_file para cada PDF encontrado
                self.add_context_file(os.path.join(folder_path, file), thread_id)



    def start_thread(self, thread_id: str):
        """
        Inicia uma nova thread de conversação.
        
        Args:
            thread_id (str): O ID da thread a ser criada.
        
        Raises:
            ValueError: Se a thread já existir.
        """
        if thread_id not in self.threads:
            self.threads[thread_id] = []
        else:
            raise ValueError(f"Thread {thread_id} já existe.")



    def get_name(self):
        """
        Retorna o nome do assistente.
        
        Returns:
            str: O nome do assistente.
        """
        return self.name

    def delete(self):
        """
        Deleta o assistente.
        """
        if self.assistant:
            self.client.beta.assistants.delete(assistant_id=self.assistant.id)
            self.assistant = None
        else:
            raise ValueError("Assistente não encontrado.")
        
    def set_api_key(self, new_api_key: str):
        """
        Atualiza a chave API do assistente.

        Args:
            new_api_key (str): A nova chave API a ser usada.
        """
        self.api_key = new_api_key
        self.client = OpenAI(api_key=self.api_key)
    def set_api_key_for_all_assistants(self, new_api_key: str):
        """
        Atualiza a chave API para todos os assistentes gerenciados.

        Args:
            new_api_key (str): A nova chave API a ser usada.
        """
        for assistant_name, assistant in self.assistants.items():
            assistant.set_api_key(new_api_key)
            print(f"Chave API atualizada para o assistente '{assistant_name}'.")