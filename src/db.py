import sqlite3
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

# database class to log inputs for data analysis maybe later
class Database:
    def __init__(self, name= 'my_database.db'):
        Logger.info("Initializing database!")
        self.conn = sqlite3.connect(name)
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
    
    
    
    