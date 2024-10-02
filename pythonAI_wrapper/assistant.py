# assistant.py

import os
from typing import List, Dict
from openai import OpenAI

class OpenAIAssistant:
    def __init__(self, api_key: str, name: str, model: str = 'gpt-4', instructions: str = ''):
        """
        Inicializa o assistente OpenAI com a chave API, nome, modelo e instruções iniciais.

        Args:
            api_key (str): A chave API da OpenAI para autenticação.
            name (str): O nome do assistente.
            model (str, optional): O modelo de linguagem a ser usado. Padrão é 'gpt-4'.
            instructions (str, optional): Instruções iniciais para o assistente. Padrão é uma string vazia.

        Raises:
            ValueError: Se a chave API for inválida.
            openai.error.InvalidRequestError: Se houver um problema ao criar o assistente na API da OpenAI.
        """
        self.client = OpenAI(api_key=api_key)
        self.name = name
        self.model = model
        self.instructions = instructions
        self.context_files: List[str] = []
        self.threads: Dict[str, List[Dict]] = {}
        self.assistant = self.client.beta.assistants.create(
            name=name,
            instructions=instructions,
            model=model
        )

    
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
        try:
            os.makedirs(thread_dir, exist_ok=True)
        except OSError as e:
            print(f"Error creating directory {thread_dir}: {e}")
            raise
        # Get the filename from the original path
        file_name = os.path.basename(file_path)

        # Create the new file path in the thread directory
        new_file_path = os.path.join(thread_dir, file_name)

        client = OpenAI()  # Add this line

        with open(file_path, "rb") as source_file:
            with open(new_file_path, "wb") as dest_file:
                dest_file.write(source_file.read())
        file_object = client.files.create(
            file=open("path/to/your/file", "rb"),
            purpose="assistants"
        )

        content="",
        file_ids=[file_object.id]
        # Add the file to the thread
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
        Envia um prompt para uma thread existente.
        
        Args:
            thread_id (str): O ID da thread a ser usada.
            prompt (str): O prompt a ser enviado.
        
        Returns:
            str: A resposta do assistente.
        """
        if thread_id in self.threads:
            thread = self.client.beta.threads.create()
            message = self.client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content=prompt
            )
            run = self.client.beta.threads.runs.create(
                thread_id=thread.id,
                assistant_id=self.assistant.id
            )
            run = self.client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
            while run.status != "completed":
                run = self.client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
            
            messages = self.client.beta.threads.messages.list(thread_id=thread.id)
            response = messages.data[0].content[0].text.value
            self.threads[thread_id].append({"prompt": prompt, "response": response})
            return response
        else:
            raise ValueError(f"Thread {thread_id} não encontrada.")

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
