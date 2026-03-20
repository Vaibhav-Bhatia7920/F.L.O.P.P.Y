import argparse
import os
import chromadb
from loader import classify_files, read_files
from llm import construct_prompt, query_llm
from indexer import give_chunks,embed_chunks
from pathlib import Path



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder")
    parser.add_argument("--query")
    args = parser.parse_args()
    collection = chromadb.PersistentClient(path="./chromadb").get_or_create_collection(name="documents")
    files = os.listdir(args.folder)
    print(files)
    print(args.folder)
    chunks  =  give_chunks(Path(args.folder))
    embeddings = embed_chunks(chunks)
    result = collection.query(
        query_texts=[args.query],
        n_results=5
    )
    context = "\n".join(result['documents'][0])
    prompt = construct_prompt(args.query, context)
    response = query_llm(prompt)
    print(response)