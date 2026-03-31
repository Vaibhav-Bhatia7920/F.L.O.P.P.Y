import requests
from loader import classify_files, read_files, chunk_files
from pathlib import Path
import chromadb
import uuid
import os


def generate_embedding(data):
    params = {"model": "nomic-embed-text:latest", "input": data}
    response = requests.post("http://localhost:11434/api/embed", json=params)
    response_data = response.json()
    if "embeddings" not in response_data:
        raise KeyError(f"'embeddings' key not found in response. Response: {response_data}")
    # print(response_data)
    return response_data["embeddings"][0]

def embed_chunks(chunks):
    embeddings = []
    
    for chunk in chunks:
        chunk_data = chunk["text"]
        print(chunk)
        params = {"model": "nomic-embed-text:latest", "input": [chunk_data]}
        response = requests.post("http://localhost:11434/api/embed", json=params)
        response_data = response.json()
        print(response_data)
        if "embeddings" not in response_data:
            raise KeyError(f"'embedding' key not found in response. Response: {response_data}")
        
        embeddings.append(response_data["embeddings"][0])
    print("This is the embeddings list:", embeddings)
    return embeddings

def add_to_db(path):
    collection = chromadb.PersistentClient(path="./chromadb").get_or_create_collection(name="documents")
    all_chunks = chunk_files(path)
    
    embeddings = embed_chunks(all_chunks)
    for ind in range(len(all_chunks)):
        collection.add(
            documents=[all_chunks[ind]["text"]],
            embeddings=[embeddings[ind]],
            metadatas=[{
            "source": all_chunks[ind]["source"],
            "path": all_chunks[ind]["path"],
            }],
            ids=[f"chunk_{ind}"]
        )
    
if __name__ == "__main__":
    directory = Path('.')
    print(directory)
    print(list(directory.iterdir()))
    client = chromadb.PersistentClient(path="./chromadb")
    collection = client.get_or_create_collection(name="documents")

    all_chunks = chunk_files((directory))
    embeddings = embed_chunks(all_chunks)

    assert len(all_chunks) == len(embeddings), "Mismatch in chunks and embeddings"

    print(f"Total chunks: {len(all_chunks)}")

    collection.add(
        documents=[chunk["text"] for chunk in all_chunks],
        embeddings=embeddings,
        metadatas=[
            {
                "source": chunk["source"],
                "path": chunk["path"],
            } for chunk in all_chunks
        ],
        ids=[str(uuid.uuid4()) for _ in all_chunks]
    )