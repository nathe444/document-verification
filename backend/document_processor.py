import docx
import PyPDF2
import io
import zipfile
import xml.etree.ElementTree as ET

class DocumentProcessor:
    @staticmethod
    def extract_text(file):
        """
        Extract text from different document types
        Supports: .txt, .docx, .pdf
        """
        # Reset file pointer
        file.seek(0)
        
        # Determine file type
        file_extension = file.filename.lower().split('.')[-1]
        
        try:
            if file_extension == 'txt':
                return file.read().decode('utf-8')
            
            elif file_extension == 'docx':
                # Handle DOCX files 
                with zipfile.ZipFile(file) as zf:
                    xml_content = zf.read('word/document.xml')
                    tree = ET.fromstring(xml_content)
                    
                    # Extract text from XML
                    text_parts = []
                    for elem in tree.iter():
                        if elem.tag.endswith('}t'):  # Text tag in DOCX XML
                            if elem.text:
                                text_parts.append(elem.text)
                    
                    return '\n'.join(text_parts)
            
            elif file_extension == 'pdf':
                pdf_reader = PyPDF2.PdfReader(file)
                text = ''
                for page in pdf_reader.pages:
                    text += page.extract_text() + '\n'
                return text.strip()
            
            else:
                raise ValueError(f"Unsupported file type: {file_extension}")
        
        except Exception as e:
            raise ValueError(f"Error processing file: {str(e)}")