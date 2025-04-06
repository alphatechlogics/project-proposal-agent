import PyPDF2
from docx import Document
import io

class DocumentProcessor:
    def process_document(self, uploaded_file):
        file_type = uploaded_file.name.split('.')[-1].lower()
        content = ""
        
        if file_type == 'pdf':
            content = self._process_pdf(uploaded_file)
        elif file_type == 'docx':
            content = self._process_docx(uploaded_file)
        elif file_type == 'txt':
            content = uploaded_file.getvalue().decode('utf-8')
            
        return self._structure_content(content)
    
    def _process_pdf(self, file):
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file.getvalue()))
        return " ".join(page.extract_text() for page in pdf_reader.pages)
    
    def _process_docx(self, file):
        doc = Document(io.BytesIO(file.getvalue()))
        return " ".join(paragraph.text for paragraph in doc.paragraphs)
    
    def _structure_content(self, content):
        # Basic content structuring
        sections = {
            "overview": "",
            "requirements": [],
            "constraints": [],
            "specifications": []
        }
        
        # Simple section detection (can be enhanced with ML/regex)
        lines = content.split('\n')
        current_section = "overview"
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Basic section detection
            lower_line = line.lower()
            if "requirement" in lower_line:
                current_section = "requirements"
                continue
            elif "constraint" in lower_line:
                current_section = "constraints"
                continue
            elif "specification" in lower_line:
                current_section = "specifications"
                continue
                
            # Add content to appropriate section
            if current_section in ["requirements", "constraints", "specifications"]:
                sections[current_section].append(line)
            else:
                sections["overview"] += line + " "
                
        return sections