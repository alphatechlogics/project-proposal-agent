import PyPDF2
from docx import Document
from utils import batch_process
from loguru import logger

class DocumentProcessor:
    def __init__(self, chunk_size=4000):
        self.chunk_size = chunk_size

    def process_document(self, file):
        file_extension = file.name.split('.')[-1].lower()
        
        try:
            if file_extension == 'pdf':
                return self._process_pdf(file)
            elif file_extension == 'docx':
                return self._process_docx(file)
            elif file_extension == 'txt':
                return self._process_txt(file)
            else:
                raise ValueError(f"Unsupported file format: {file_extension}")
        except Exception as e:
            logger.error(f"Error processing document: {str(e)}")
            raise

    def _process_pdf(self, file):
        pdf_reader = PyPDF2.PdfReader(file)
        text_chunks = []
        
        for page in pdf_reader.pages:
            text = page.extract_text()
            if text.strip():
                text_chunks.extend(self._split_into_chunks(text))
        
        return self._combine_chunks(text_chunks)

    def _process_docx(self, file):
        doc = Document(file)
        text_chunks = []
        
        for paragraph in doc.paragraphs:
            text = paragraph.text
            if text.strip():
                text_chunks.extend(self._split_into_chunks(text))
                
        return self._combine_chunks(text_chunks)

    def _process_txt(self, file):
        text = file.read().decode('utf-8')
        text_chunks = self._split_into_chunks(text)
        return self._combine_chunks(text_chunks)

    def _split_into_chunks(self, text):
        words = text.split()
        chunks = []
        current_chunk = []
        current_length = 0
        
        for word in words:
            word_length = len(word) + 1  # +1 for space
            if current_length + word_length > self.chunk_size:
                chunks.append(' '.join(current_chunk))
                current_chunk = [word]
                current_length = word_length
            else:
                current_chunk.append(word)
                current_length += word_length
                
        if current_chunk:
            chunks.append(' '.join(current_chunk))
            
        return chunks

    def _combine_chunks(self, chunks):
        def merge_batch(batch):
            return [' '.join(batch)]
            
        # Process chunks in batches of 5
        return batch_process(chunks, 5, merge_batch)[0]