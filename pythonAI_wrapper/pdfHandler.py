# pdfHandler.py

import fitz  # PyMuPDF

class PDFHandler:
    def read_pdf(file_path):
        """Lê o conteúdo de um arquivo PDF e retorna o texto."""
        text = ""
        try:
            with fitz.open(file_path) as pdf_document:
                for page in pdf_document:
                    text += page.get_text()  # Lê o texto de cada página
        except Exception as e:
            print(f"Erro ao ler o arquivo PDF: {e}")
        
        return text
