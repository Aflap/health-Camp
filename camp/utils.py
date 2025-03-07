# camp/utils.py
# camp/utils.py
from PyPDF2 import PdfReader

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    try:
        reader = PdfReader(pdf_path)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        print(f"❌ Error extracting text from PDF: {e}")
        return None
