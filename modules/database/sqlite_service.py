import json
import sqlite3
from sqlite3 import Connection, Error
from typing import List

from modules.machine.machine import Machine


def sql_connection() -> Connection:
    """Establish the sql connection."""
    try:
        con = sqlite3.connect("mydatabase.db", check_same_thread=False)
        return con
    except Error:
        print(Error)


class DatabaseService:
    """A database service that is doing SQL jobs/query."""

    def __init__(self):
        """Establish a connection, then do a SQL migration."""
        self.con = sql_connection()
        self.con.row_factory = sqlite3.Row
        self.init_table()

    def init_table(self) -> None:
        """Start SQL migration to create a machine table."""
        cursor_obj = self.con.cursor()
        cursor_obj.execute(
            "CREATE TABLE IF NOT EXISTS machines(id INTEGER PRIMARY KEY "
            "AUTOINCREMENT, name text, location text, stock text)"
        )
        self.con.commit()

    def insert_into_machine(self, machine: Machine) -> int:
        """Insert a machine object into a machine table."""
        cursor_obj = self.con.cursor()
        stocks_text = json.dumps(machine.stocks)
        cursor_obj.execute(
            "INSERT INTO machines (name, location, stock) VALUES(?, ?, ?)",
            (machine.name, machine.location, stocks_text),
        )
        self.con.commit()
        return cursor_obj.lastrowid

    def get_all_machines(self) -> List[Machine]:
        """Query all machine from the machine table."""
        cursor_obj = self.con.cursor()
        cursor_obj.execute("SELECT * FROM machines")
        instance_from_database = cursor_obj.fetchall()
        machines = [dict(row) for row in instance_from_database]
        for machine in machines:
            machine["stock"] = json.loads(machine["stock"])
        return machines

    def update_stock(self, machine_id: int, new_stock: dict[str, int]):
        """Update the stock of a machine."""
        cursor_obj = self.con.cursor()
        stocks_text = json.dumps(new_stock)
        cursor_obj.execute(
            "UPDATE machines SET stock = ? WHERE id = ?", (stocks_text, machine_id)
        )
        self.con.commit()

    def delete_machine_by_id(self, machine_id: int):
        """Delete the machine by its id in a machine table."""
        cursor_obj = self.con.cursor()
        cursor_obj.execute("DELETE FROM machines WHERE id = ?", (machine_id,))
        self.con.commit()

    def get_machine_by_id(self, machine_id: int) -> dict:
        """Get a machine by its id."""
        cursor_obj = self.con.cursor()
        cursor_obj.execute("SELECT * FROM machines where id = ?", (machine_id,))
        instance_from_database = cursor_obj.fetchone()
        machine = dict(instance_from_database)
        machine["stock"] = json.loads(instance_from_database["stock"])
        return machine


db = DatabaseService()
