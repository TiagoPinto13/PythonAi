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

    def get_response(self, prompt: str):
        """Obtém uma resposta do assistente para um prompt dado."""
        # A estrutura de mensagens deve ser atualizada para o novo formato da API.
        response = self.client.chat.completions.create(  # Usar self.client
            model=self.model,
            messages=[
                {"role": "system", "content": self.instructions},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content



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

        with open(file_path, "rb") as source_file:
            with open(new_file_path, "wb") as dest_file:
                dest_file.write(source_file.read())
        
        # Adiciona o arquivo ao sistema
        file_object = self.client.files.create(  # Usar self.client
            file=open(new_file_path, "rb"),  # Corrigido para usar new_file_path
            purpose="assistants"
        )

        # Adicionar o arquivo à thread
        self.client.beta.threads.messages.create(  # Usar self.client
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

    def send_prompt(self, thread_id: str, prompt: str):
        """
        Envia um prompt para o assistente na thread especificada.

        Args:
            thread_id (str): ID da thread na qual enviar o prompt.
            prompt (str): O prompt a ser enviado.

        Returns:
            str: Resposta do assistente.
        
        Raises:
            ValueError: Se a thread não for encontrada.
        """
        if thread_id not in self.threads:
            raise ValueError(f"Thread {thread_id} não encontrada.")

        # Obter a resposta
        response = self.get_response(prompt)

        # Adiciona a mensagem e a resposta ao histórico da thread
        self.threads[thread_id].append({"role": "user", "content": prompt})
        self.threads[thread_id].append({"role": "assistant", "content": response})

        return response


    def get_thread_history(self, thread_id: str):
        """
        Retorna o histórico da thread.
        
        Args:
            thread_id (str): O ID da thread a ser usada.
        
        Returns:
            List[Dict]: O histórico da thread.
        """
        if thread_id in self.threads:
            return self.threads[thread_id]
        else:
            raise ValueError(f"Thread {thread_id} não encontrada.")

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
