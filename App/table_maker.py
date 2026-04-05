import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def create_table(table_name="coversations"):
    conn = psycopg2.connect(
        host="localhost",
        database="Floppy DB",
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )
    cursor = conn.cursor()
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id SERIAL PRIMARY KEY,
            session_id UUID,
            user_name TEXT,
            user_content TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    create_table("conversations")