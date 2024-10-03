# pdfHandler.py

import os

class PDFHandler:
    def read_pdf(self,file_path):
        """Lê o conteúdo de um arquivo PDF e retorna o texto."""
        prompt = ""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                prompt += content + "\n"
        except Exception as e:
            print(f"Erro ao ler o arquivo PDF: {e}")
        
        return prompt
    def read_folder(self,folder_path):
        """Lê o conteúdo de um diretório e retorna o texto."""
        prompt = ""
        try:
            for file_name in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file_name)
                if os.path.isfile(file_path) and file_name.endswith('.pdf'):
                    prompt += self.read_pdf(file_path) + "\n"
        except Exception as e:
            print(f"Erro ao ler o diretório: {e}")
        
        return prompt
    
    
