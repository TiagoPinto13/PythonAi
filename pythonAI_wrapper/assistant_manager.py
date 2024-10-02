# assistant_manager.py

from pythonAI_wrapper.assistant import OpenAIAssistant

class AssistantManager:
    def __init__(self):
        self.assistants = {}

    def create_assistant(self, api_key: str, name: str, model: str = 'gpt-4', instructions: str = ''):
        """
        Cria um novo assistente com o nome fornecido.

        Args:
            api_key (str): A chave da API para autenticar o assistente.
            name (str): Nome do assistente.
            model (str): Modelo do OpenAI a ser usado. Padrão é 'gpt-4'.
            instructions (str): Instruções iniciais para o assistente.

        Raises:
            ValueError: Se já existir um assistente com o mesmo nome.
        """
        if name in self.assistants:
            raise ValueError(f"Já existe um assistente com o nome '{name}'.")
        
        # Criação de um novo assistente
        self.assistants[name] = OpenAIAssistant(api_key=api_key, name=name, model=model, instructions=instructions)

    def get_assistant(self, name: str) -> OpenAIAssistant:
        """
        Retorna um assistente pelo nome.

        Args:
            name (str): Nome do assistente.

        Returns:
            OpenAIAssistant: O objeto do assistente correspondente.

        Raises:
            ValueError: Se não for encontrado um assistente com o nome fornecido.
        """
        if name not in self.assistants:
            raise ValueError(f"Nenhum assistente encontrado com o nome '{name}'.")
        return self.assistants[name]

    def list_assistants(self) -> list:
        """
        Lista todos os assistentes criados.

        Returns:
            list: Uma lista com os nomes de todos os assistentes criados.
        """
        if not self.assistants:
            return ["Nenhum assistente criado."]
        
        return [f"Nome: {name}, Modelo: {self.assistants[name].model}" for name in self.assistants]

    def remove_assistant(self, name):
        """
        Remove um assistente pelo nome.

        Args:
            name (str): Nome do assistente a ser removido.

        Raises:
            ValueError: Se o assistente com o nome fornecido não for encontrado.
        """
        if name in self.assistants:
            self.assistants[name].delete()
            del self.assistants[name]
        else:
            raise ValueError(f"Assistant '{name}' not found")
