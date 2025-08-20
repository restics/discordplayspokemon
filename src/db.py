import sqlite3
import os
from pydantic import BaseModel, ValidationError
from logger import Logger

class MovesInput(BaseModel):
    userid : int
    input : str

class MovesEntry(BaseModel):
    id: int
    userid : int
    input : str
    creation_time : int

db_dir = 'data'

# database class to log inputs for data analysis maybe later
class Database:
    def __init__(self, name= 'input_logs.db'):
        Logger.info("Initializing database!")
        os.makedirs(db_dir, exist_ok=True)
        
        self.conn = sqlite3.connect(os.path.join(db_dir, name))
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS moves (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            userid INTEGER,
            input VARCHAR(10),
            created_at INTEGER DEFAULT (strftime('%s', 'now'))
        );''')
        Logger.info("Database initialized!")

    # adds a user input entry to the database
    def add_entry(self, userid, inputs):
        if not self.conn or not self.cursor:
            Logger.warning("Database not available, skipping log entry")
            return
            
        try:
            validated_input = MovesInput(userid=userid, input=inputs)
            self.cursor.execute('''INSERT INTO moves (userid, input) VALUES (:userid, :input)''',
            {
                'userid' : validated_input.userid,
                'input' : validated_input.input
            })
            self.conn.commit()

        except ValidationError as e:
            for error in e.errors():
                field = error['loc'][0] # which input field failed
                message = error['msg'] 
                Logger.error('Error in %s: %s', field, message)
        except Exception as e:
            Logger.error("Database error: %s", e)
    
    
    
    