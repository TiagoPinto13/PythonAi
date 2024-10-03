# test_assistant.py

# Adicionar o diretório principal ao caminho do Python
import os
import sys

from pythonAI_wrapper.pdfHandler import PDFHandler

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import OPENAI_API_KEY
from pythonAI_wrapper.assistant_manager import AssistantManager


# Inicializa o AssistantManager
manager = AssistantManager()

# Nome do assistente que será usado
assistant_name = "MeuAssistente"

# Criação de um assistente (se necessário)
# manager.create_assistant(OPENAI_API_KEY, assistant_name, "gpt-4", "Você é um assistente de teste")

thread_id = "minha_thread"

# Criar uma thread para o assistente (se necessário)
# thread_id = manager.create_thread(assistant_name, thread_id)

# Enviar um prompt simples
prompt = "E a dA ALEMANHA?"
response = manager.send_prompt(assistant_name, thread_id, prompt)

# Exibir a resposta do assistente ao prompt simples
print(f"Resposta do assistente: {response}\n")

print("-----------------------------------\n")
pdf_handler = PDFHandler()
content = pdf_handler.read_pdf('files/test.pdf')
print(content)

print("-----------------------------------\n")
file_path = "files/test.pdf"  # Substitua pelo caminho absoluto
if os.path.exists(file_path):
    print("O arquivo existe.")
else:
    print("O arquivo não foi encontrado.")

print("-----------------------------------\n")


file_path = "files/test.pdf"
print(f"Caminho absoluto: {os.path.abspath(file_path)}")


print("-----------------------------------\n")
# Enviar um ficheiro específico para o contexto da thread
file_path = "files/test.pdf"

try:
    file_id = manager.get_assistant(assistant_name).add_context_file(file_path, thread_id)
    print(f"Ficheiro {file_path} enviado para a thread {thread_id} com o ID {file_id}")
except Exception as e:
    print(f"Erro ao enviar o ficheiro: {e}")

# Enviar uma pasta de ficheiros PDF
folder_path = "files/pdf_folder"

try:
    manager.get_assistant(assistant_name).add_context_folder(folder_path, thread_id)
    print(f"Todos os ficheiros PDF da pasta {folder_path} foram enviados para a thread {thread_id}")
except Exception as e:
    print(f"Erro ao enviar a pasta: {e}")

# Exibir a resposta do assistente após o envio do ficheiro/pasta
response = manager.send_prompt(assistant_name, thread_id, "Aqui estão alguns documentos importantes para revisar.")
print(f"Resposta do assistente após o envio dos documentos: {response}\n")

# Visualizar o histórico completo da thread
# history = manager.get_thread_history(assistant_name, thread_id)
# print(f"Histórico da thread: {history}")
