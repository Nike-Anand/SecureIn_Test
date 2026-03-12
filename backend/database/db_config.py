import mysql.connector

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  
    'database': 'cpe_database'
}

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)
