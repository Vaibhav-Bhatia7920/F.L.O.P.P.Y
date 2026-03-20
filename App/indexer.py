import requests
from loader import classify_files, read_files, chunk_files
from pathlib import Path
import chromadb

def give_chunks(Path):
    pdf_files, docx_files, txt_files = classify_files(Path)
    pdf_content, docx_content, txt_content = read_files(pdf_files, docx_files, txt_files)
    pdf_chunks, docx_chunks, txt_chunks = chunk_files(pdf_content, docx_content, txt_content)
    all_chunks = pdf_chunks + docx_chunks + txt_chunks
    return all_chunks

def embed_chunks(chunks):
    params = {"model" : "llama3.1:latest" , "prompt" : "Your chunks text here", "stream" : False}
    response = requests.post("http://localhost:11434/api/embeddings", json=params)
    return response.json

if __name__ == "__main__":
    directory = Path('.')
    collection = chromadb.PersistentClient(path="./chromadb").get_or_create_collection(name="documents")
    all_chunks = give_chunks(directory)
    response = embed_chunks(all_chunks)

    for ind in range(len(all_chunks)):
        collection.add(
            documents=[all_chunks[ind]],
            embeddings=[response[ind]],
            ids=[f"chunk_{ind}"]
        )
    print(response)