#snippet.py

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
manager.create_assistant(OPENAI_API_KEY, assistant_name, "gpt-4", "Você é um assistente de teste")

thread_id = "minha_thread"

# Criar uma thread para o assistente (se necessário)
thread_id = manager.create_thread(assistant_name, thread_id)

# Enviar um prompt simples
prompt = "Qual a capital do Brasil?"
response = manager.send_prompt(assistant_name, thread_id, prompt)

prompt = "E a da Alemanha?"
response = manager.send_prompt(assistant_name, thread_id, prompt)

# Exibir a resposta do assistente ao prompt simples
print(f"Resposta do assistente: {response}\n")


print("-----------------------------------\n")
pdf_handler = PDFHandler()
content = pdf_handler.read_pdf('files/test.pdf')
print(content)

response = manager.send_prompt(assistant_name, thread_id, content)
print(f"Resposta do assistente: {response}\n")

print("-----------------------------------\n")



content = pdf_handler.read_pdf('files/test2.pdf')
print(content)

response = manager.send_prompt(assistant_name, thread_id, content)
print(f"Resposta do assistente: {response}\n")

print("-----------------------------------\n")
content = pdf_handler.read_folder('files')
print(content)



response = manager.send_prompt(assistant_name, thread_id, content)
print(f"Resposta do assistente: {response}\n")

print("-----------------------------------\n")



# Visualizar o histórico completo da thread
history = manager.get_thread_history(assistant_name, thread_id)
print(f"Histórico da thread: {history}")

print("-----------------------------------\n")

# Ver todos os assistentes
assistants = manager.list_assistants()
print(f"Assistents: {assistants}")

print("-----------------------------------\n")

# Ver todos os threads
threads = manager.list_threads(assistant_name)
print(f"Threads: {threads}")

