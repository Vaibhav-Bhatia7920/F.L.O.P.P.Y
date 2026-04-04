import psycopg2
import os
import uuid

def add_to_memory(conversation):
    conn = psycopg2.connect(
        host="localhost",
        database="Floppy DB",
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )
    cursor = conn.cursor()
    id = str(uuid.uuid4())
    user_type = conversation.user
    user_text = conversation.content

    cursor.execute("""
        INSERT INTO coversations (id,session_id, user, user_content)
        VALUES (%s, %s, %s, %s)
    """, (id, conversation.session_id, user_type, user_text))
    conn.commit()
    cursor.close()
    conn.close()


def get_memory(session_id):
    conn = psycopg2.connect(
        host="localhost",
        database="Floppy DB",
        user=os.getenv("POSTGRES_USER"),    
        password=os.getenv("POSTGRES_PASSWORD")
    )
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT user, user_content FROM coversations
        WHERE session_id = %s""", (session_id,))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results