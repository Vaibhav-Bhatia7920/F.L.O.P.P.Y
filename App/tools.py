from pathlib import Path
from loader import chunk_files
from sklearn.metrics.pairwise import cosine_similarity
from llm import query_llm
import chromadb

def list_files(directory):
    return [str(f) for f in Path(directory).iterdir() if f.is_file()]

def read_file(file_path):
    with open(Path(file_path),'r') as f:
        return f.read()
    
def search_files(directory, query):
    
    collection = chromadb.PersistentClient(path="./chromadb").get_or_create_collection(name="documents")
    result = collection.query(
        query_texts=[query],
        n_results=1
    )
    
    return result["documents"][0][0], result["metadatas"][0][0]["path"]
    # chunks = chunk_files(directory)
    # embeddings = embed_chunks(chunks)
    # query_embedding = generate_embedding(query)
    # max_sim_score = 0
    # for ind in range(len(embeddings)):
    #     vector_a = [embeddings[ind]]
    #     vector_b = [query_embedding]
    #     similarity_matrix = cosine_similarity(vector_a, vector_b)
    #     similarity_score = similarity_matrix[0][0]
    #     if similarity_score > max_sim_score:
    #         chunk_needed = chunks[ind]
    #         max_sim_score = similarity_score
    
    # return chunk_needed["path"]        
    
    
def summarize_file(file_path):
    content = read_file(file_path)
    prompt = f"""
    Summarize the following content:
    {content}
    """
    summary = query_llm(prompt)
    return summary
        
    
    
    