import chromadb

if __name__ == "__main__":
    client = chromadb.PersistentClient(path="./chromadb")
    collection = client.get_or_create_collection(name="documents")