import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def create_table():
    conn = psycopg2.connect(
        host="localhost",
        database="Floppy DB",
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS coversations (
            id SERIAL PRIMARY KEY,
            session_id UUID,
            user TEXT,
            user_content TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()
