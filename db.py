import sqlite3

def init_db():
    connection = sqlite3.connect("templates/ashfordrecords.db")
    cursor = connection.cursor()
    cursor.execute("""
       CREATE TABLE IF NOT EXISTS users (
       USERid INTEGER PRIMARY KEY AUTOINCREMENT,
       username TEXT UNIQUE,
       email TEXT UNIQUE,
       password_hash TEXT    
    ) 
    """)
    connection.commit()
    connection.close()

init_db()
#COPY AND PASTE PARTS OF THE ABOVE CODE 2 TIMES TO CREATE THE OTHER TABLE TO MAKE SURE THAT "IF NOT EXISTS" IS BEING USED EACH TIME. MAKE SURE TO LABEL PRIMARY AND FOREIGN KEYS PROPERLY WITH THE CODE
def db_connection():
    connection = sqlite3.connect("templates/ashfordrecords.db")
    connection.row_factory = sqlite3.Row
    return connection