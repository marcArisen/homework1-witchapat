import json
import sqlite3
from sqlite3 import Error

from modules.machine import Machine

class Database_Service:
    def __init__(self):
        self.con = self.sql_connection()
        self.con.row_factory = sqlite3.Row
        self.init_table()
    
    def sql_connection(self):
        try:
            con = sqlite3.connect('mydatabase.db', check_same_thread=False)
            return con
        except Error:
            print(Error)
        
    def init_table(self):
        cursorObj = self.con.cursor()
        cursorObj.execute("CREATE TABLE IF NOT EXISTS machines(id INTEGER PRIMARY KEY AUTOINCREMENT, name text, location text, stock text)")
        self.con.commit()
    
    def insert_into_machine(self, machine):
        cursorObj = self.con.cursor()
        stocks_text = json.dumps(machine.stocks)
        cursorObj.execute("INSERT INTO machines (name, location, stock) VALUES('%s', '%s', '%s')" %(machine.name, machine.location, stocks_text))
        self.con.commit()
        return cursorObj.lastrowid

    def get_all_machines(self):
        cursorObj = self.con.cursor()
        cursorObj.execute("SELECT * FROM machines")
        rows = cursorObj.fetchall()
        to_return = [dict(row) for row in rows]
        for machine in to_return:
            machine['stock'] = json.loads(machine['stock'])
        return to_return
    
    def update_stock(self, machine_id, new_stock):
        cursorObj = self.con.cursor()
        stocks_text = json.dumps(new_stock)
        cursorObj.execute("UPDATE machines SET stock = ? WHERE id = ?", (stocks_text, machine_id))
        self.con.commit()
    
    def delete_machine(self, machine_id):
        cursorObj = self.con.cursor()
        cursorObj.execute("DELETE FROM machines WHERE id = ?", (machine_id))
        self.con.commit()
    
    def get_by_id(self, machine_id):
        cursorObj = self.con.cursor()
        cursorObj.execute("SELECT * FROM machines where id = ?", (machine_id,))
        r = cursorObj.fetchone()
        to_return = dict(r)
        to_return['stock'] = json.loads(to_return['stock'])
        return to_return

db = Database_Service()

