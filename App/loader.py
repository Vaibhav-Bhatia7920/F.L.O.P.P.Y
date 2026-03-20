from pypdf import PdfReader
from docx import Document
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter  

def classify_files(directory):
    pdf, docx, txt = [], [], []
    for file in directory.iterdir():
        if file.is_file():
            if str(file).endswith('.pdf'):
                pdf.append(file)
            elif str(file).endswith('.docx'):
                docx.append(file)
            elif str(file).endswith('.txt'):
                txt.append(file)
    return pdf, docx, txt

def read_files(pdf_files, docx_files, txt_files):
    pdf_content, docx_content, txt_content = [], [], []
    for pdf in pdf_files:
        reader = PdfReader(pdf)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
        pdf_content.append(text)
    for docx in docx_files:
        doc = Document(docx)
        text = ''
        for para in doc.paragraphs:
            text += para.text + '\n'
        docx_content.append(text)
    for txt in txt_files:
        with open(txt, 'r') as f:
            txt_content.append(f.read())
    return pdf_content, docx_content, txt_content


def chunk_files(pdf_content, docx_content, txt_content):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    pdf_chunks = [text_splitter.create_documents([content]) for content in pdf_content]
    docx_chunks = [text_splitter.create_documents([content]) for content in docx_content]
    txt_chunks = [text_splitter.create_documents([content]) for content in txt_content]
    return pdf_chunks, docx_chunks, txt_chunks

if __name__ == "__main__":
    directory = Path('path/to/your/directory')
    pdf_files, docx_files, txt_files = classify_files(directory)
    pdf_content, docx_content, txt_content = read_files(pdf_files, docx_files, txt_files)       