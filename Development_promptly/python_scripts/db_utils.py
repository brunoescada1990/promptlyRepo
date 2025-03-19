import os
import logging
import psycopg2
from dotenv import load_dotenv


load_dotenv()

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
}


def get_connection():
    """
    Establishes a connection to the PostgreSQL database.
    """
    
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        logging.error(f"Error connecting to the database: {e}")
        raise