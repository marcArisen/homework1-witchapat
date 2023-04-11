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
        self.init_stock_history_table()

    def init_table(self) -> None:
        """Start SQL migration to create a machine table."""
        cursor_obj = self.con.cursor()
        cursor_obj.execute(
            "CREATE TABLE IF NOT EXISTS machines(id INTEGER PRIMARY KEY "
            "AUTOINCREMENT, name text, location text, stock text)"
        )
        self.con.commit()

    def init_stock_history_table(self) -> None:
        """Create a stock_history table."""
        cursor_obj = self.con.cursor()
        cursor_obj.execute(
            "CREATE TABLE IF NOT EXISTS stock_history(id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "machine_id INTEGER, timestamp DATETIME, product_name text, quantity INTEGER)"
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

        # Insert stock history data
        for product_name, quantity in new_stock.items():
            self.insert_stock_history(machine_id, product_name, quantity)

    def delete_machine_by_id(self, machine_id: int):
        """Delete the machine by its id in a machine table."""
        cursor_obj = self.con.cursor()
        cursor_obj.execute("DELETE FROM machines WHERE id = ?", (machine_id,))
        self.con.commit()

    def get_machine_by_id(self, machine_id: int) -> dict:

        cursor_obj = self.con.cursor()
        cursor_obj.execute("SELECT * FROM machines where id = ?", (machine_id,))
        instance_from_database = cursor_obj.fetchone()
        machine = dict(instance_from_database)
        machine["stock"] = json.loads(instance_from_database["stock"])
        return machine

    def insert_stock_history(
        self, machine_id: int, product_name: str, quantity: int
    ) -> int:
        """Insert stock history data."""
        cursor_obj = self.con.cursor()
        cursor_obj.execute(
            "INSERT INTO stock_history (machine_id, timestamp, product_name, quantity) VALUES(?, datetime('now'), ?, ?)",
            (machine_id, product_name, quantity),
        )
        self.con.commit()
        return cursor_obj.lastrowid

    def get_stock_history_by_product_name(self, product_name: str):
        """Get stock history by product_name."""
        cursor_obj = self.con.cursor()
        cursor_obj.execute(
            "SELECT * FROM stock_history WHERE product_name = ? ORDER BY timestamp ASC",
            (product_name,),
        )
        rows = cursor_obj.fetchall()
        return [dict(row) for row in rows]

    def get_stock_history_by_machine_id_grouped_by_timestamp(self, machine_id: int):
        """Get stock history by machine_id, grouped by timestamp."""
        cursor_obj = self.con.cursor()
        cursor_obj.execute(
            "SELECT timestamp, product_name, SUM(quantity) as quantity FROM stock_history "
            "WHERE machine_id = ? GROUP BY timestamp, product_name ORDER BY timestamp ASC",
            (machine_id,),
        )
        rows = cursor_obj.fetchall()

        # Group the stock history data by timestamp
        grouped_data = {}
        for row in rows:
            timestamp = row["timestamp"]
            if timestamp not in grouped_data:
                grouped_data[timestamp] = {}
            grouped_data[timestamp][row["product_name"]] = row["quantity"]

        return grouped_data


db = DatabaseService()
