import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "your-server.postgres.database.azure.com"),
        database=os.getenv("DB_NAME", "clinicdb"),
        user=os.getenv("DB_USER", "your_user@your-server"),
        password=os.getenv("DB_PASS", "your_password"),
        port=os.getenv("DB_PORT", "5432"),
        cursor_factory=RealDictCursor
    )
