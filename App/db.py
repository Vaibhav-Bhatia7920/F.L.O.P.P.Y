import chromadb

path = "./chromadb"
client = chromadb.PersistentClient(path=path)
collection = client.get_or_create_collection(name="documents")