from fastapi import FastAPI
import psycopg2
import os
import chromadb
from dotenv import load_dotenv
from pydantic import BaseModel
from agent import agent_loop
from memory import add_to_memory, get_memory
from indexer import add_to_db

load_dotenv()
app = FastAPI()

conn = psycopg2.connect(
    host = "localhost",
    database = "Floppy DB",
    user = os.getenv("POSTGRES_USER"),
    password = os.getenv("POSTGRES_PASSWORD")
)
curson = conn.cursor()


class UserInput(BaseModel):
    message: str
    
class SessionResponse(BaseModel):
    session_flow : list

class SessionInfo(BaseModel):
    session_id: str
    user: str
    content: str

class IndexResponse(BaseModel):
    files : list
    

@app.post("/chat")
def chat(user_input : UserInput):
    response = agent_loop(user_input.message)
    ## Need to add to memory here, also need to figure out how to pass session_id here as well
    ## This will be an endpoint  that will host html page with chat interface and on clincking javascript will implement fucntion and send response to this endpoint and then display the response on the html page
    return {"response": response}

@app.post("/session")
def post_session(session_info : SessionInfo):
    add_to_memory(session_info)
    return {"message": "Session info added to memory"}

@app.post("/index")
def index_files(Path: str):
    add_to_db(Path)
    return {"message": "Files indexed successfully"}

@app.get("/index/files")
def get_indexed_files(Path: str):
    collection = chromadb.PersistentClient(path="./chromadb").get_or_create_collection(name="documents")
    results = collection.get(where ={"path": Path})
    return results

@app.get("/session")
def get_session(session_id: str):
    sessions = get_recent_sessions()
    ## This will be an endpoint that will return all the recent sessions with session_id and user name and timestamp, and on clicking on any session it will call the get_session endpoint with session_id and then return the entire session flow for that session_id
    return {"Sessions": sessions}

@app.get("/session/{session_id}")
def get_session(session_id: str):
    memory = get_memory(session_id)
    return {"memory": SessionResponse(session_flow=memory)}