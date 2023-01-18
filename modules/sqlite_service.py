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

    def get_all(self):
        cursorObj = self.con.cursor()
        cursorObj.execute("SELECT * FROM machines")
        rows = cursorObj.fetchall()
        return [dict(row) for row in rows]

    def get_by_id(self, machine_id):
        cursorObj = self.con.cursor()
        cursorObj.execute("SELECT * FROM machines where id = ?", (machine_id))
        r = cursorObj.fetchone()
        print(r)
        print(type(r))
        return dict(r)

    def print_by_row(self, rows):
        for row in rows:
            print("ID: ", row[0])
            print("name: ", row[1])
            print("location: ", row[2])
            to_dump = json.loads(row[3])
            print("stocks: ", to_dump)
            print("type of stocks:", type(to_dump))
            print("\n")
    
    def test_insert(self):
        cursorObj = self.con.cursor()
        cursorObj.execute("INSERT INTO machines VALUES(1,'Marc', 'in front of MUIC', '[yoyo, dodo]')")
        self.con.commit()
        
# a = Machine("2", "Tynu", "V condo", {"a": 1, "b": 2})
# con = sql_connection()
# init_table(con)
# insert_into_machine(con, a)
# # insert_into_machine(con, a.name, a.location, a.stocks)
# # insert_into_machine(con, "Soyjuhaha", "behind the MUIC", [0,1,2,3])
# test_fetch(con)

