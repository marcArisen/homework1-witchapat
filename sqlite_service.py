import json
import sqlite3
from sqlite3 import Error

from machine import Machine

# class Database_Service:
def sql_connection():
    try:
        con = sqlite3.connect('mydatabase.db')
        return con
    except Error:
        print(Error)
        
def init_table(con):
    cursorObj = con.cursor()
    cursorObj.execute("CREATE TABLE IF NOT EXISTS machines(id INTEGER PRIMARY KEY AUTOINCREMENT, name text, location text, stock text)")
    con.commit()
   
def insert_into_machine(con, machine):
    cursorObj = con.cursor()
    stocks_text = json.dumps(machine.stocks)
    cursorObj.execute("INSERT INTO machines (name, location, stock) VALUES('%s', '%s', '%s')" %(machine.name, machine.location, stocks_text))
    con.commit()
 
def test_insert(con):
    cursorObj = con.cursor()
    cursorObj.execute("INSERT INTO machines VALUES(1,'Marc', 'in front of MUIC', '[yoyo, dodo]')")
    con.commit()

def test_fetch(con):
    cursorObj = con.cursor()
    cursorObj.execute("SELECT * FROM machines")
    r = cursorObj.fetchall()
    # print(r)
    print_by_row(r)
    print(type(r))

def get_one_row(machine_id):
    cursorObj = con.cursor()
    cursorObj.execute("SELECT * FROM machines where id = ?", (machine_id))
    r = cursorObj.fetchone()
    print(r)
    print(type(r))

def print_by_row(rows):
    for row in rows:
            print("ID: ", row[0])
            print("name: ", row[1])
            print("location: ", row[2])
            to_dump = json.loads(row[3])
            print("stocks: ", to_dump)
            print("type of stocks:", type(to_dump))
            print("\n")
    
a = Machine("2", "Tynu", "V condo", {"a": 1, "b": 2})
con = sql_connection()
init_table(con)
insert_into_machine(con, a)
# insert_into_machine(con, a.name, a.location, a.stocks)
# insert_into_machine(con, "Soyjuhaha", "behind the MUIC", [0,1,2,3])
test_fetch(con)

