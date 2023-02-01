import json
import sqlite3
from sqlite3 import Error


def sql_connection():
    try:
        con = sqlite3.connect("mydatabase.db", check_same_thread=False)
        return con
    except Error:
        print(Error)


class DatabaseService:
    def __init__(self):
        self.con = sql_connection()
        self.con.row_factory = sqlite3.Row
        self.init_table()

    def init_table(self):
        cursorObj = self.con.cursor()
        cursorObj.execute(
            "CREATE TABLE IF NOT EXISTS machines(id INTEGER PRIMARY KEY AUTOINCREMENT, name text, location text, stock text)"
        )
        self.con.commit()

    def insert_into_machine(self, machine):
        cursorObj = self.con.cursor()
        stocks_text = json.dumps(machine.stocks)
        cursorObj.execute(
            "INSERT INTO machines (name, location, stock) VALUES(?, ?, ?)",
            (machine.name, machine.location, stocks_text),
        )
        self.con.commit()
        return cursorObj.lastrowid

    def get_all_machines(self):
        cursorObj = self.con.cursor()
        cursorObj.execute("SELECT * FROM machines")
        instance_from_database = cursorObj.fetchall()
        machines = [dict(row) for row in instance_from_database]
        for machine in machines:
            machine["stock"] = json.loads(machine["stock"])
        return machines

    def update_stock(self, machine_id, new_stock):
        cursorObj = self.con.cursor()
        stocks_text = json.dumps(new_stock)
        cursorObj.execute(
            "UPDATE machines SET stock = ? WHERE id = ?", (stocks_text, machine_id)
        )
        self.con.commit()

    def delete_machine_by_id(self, machine_id):
        cursorObj = self.con.cursor()
        cursorObj.execute("DELETE FROM machines WHERE id = ?", (machine_id))
        self.con.commit()

    def get_machine_by_id(self, machine_id):
        cursorObj = self.con.cursor()
        cursorObj.execute("SELECT * FROM machines where id = ?", (machine_id,))
        instance_from_database = cursorObj.fetchone()
        machine = dict(instance_from_database)
        machine["stock"] = json.loads(instance_from_database["stock"])
        return machine


db = DatabaseService()
