import fitz  # PyMuPDF

class PDFHandler:
    def read_pdf(self, file_path):
        try:
            doc = fitz.open(file_path)  # Abre o arquivo PDF
            content = ""
            for page in doc:
                content += page.get_text()  # Extrai texto da página
            doc.close()  # Fecha o documento
            return content.strip()  # Retorna o texto lido
        except Exception as e:
            print(f"Erro ao ler o PDF '{file_path}': {e}")
            return None
