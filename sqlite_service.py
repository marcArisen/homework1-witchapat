import json
import sqlite3
from sqlite3 import Error

def sql_connection():
    try:
        con = sqlite3.connect('mydatabase.db')
        return con
    except Error:
        print(Error)
        
def init_table(con):
    cursorObj = con.cursor()
    cursorObj.execute("CREATE TABLE IF NOT EXISTS machines(id integer PRIMARY KEY, name text, location text, stock text)")
    con.commit()
   
def insert_into_machine(con, id, name, location, stocks):
    cursorObj = con.cursor()
    stocks_text = json.dumps(stocks)
    cursorObj.execute("INSERT INTO machines VALUES( %s, '%s', '%s', '%s')" %(id, name, location, stocks_text))
    con.commit()
 
def test_insert(con):
    cursorObj = con.cursor()
    cursorObj.execute("INSERT INTO machines VALUES(1,'Marc', 'in front of MUIC', '[yoyo, dodo]')")
    con.commit()

def test_fetch(con):
    cursorObj = con.cursor()
    cursorObj.execute("SELECT * fROM machines")
    r = cursorObj.fetchall()
    print(r)
    print(type(r))
    
con = sql_connection()
init_table(con)
insert_into_machine(con, "4", "Soyjuhaha", "behind the MUIC", [1,2,4,5])
test_fetch(con)

