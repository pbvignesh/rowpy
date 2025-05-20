"""The Database module"""

from pathlib import Path
import json

class Database:
    """The Database class"""
    def __init__(self, database_name: str):
        self.tables = {}
        self.database_name = database_name
        self.data_path = Path("data")
        self.database_directory = self.data_path / self.database_name
        self.manifest_file = self.database_directory / "_db_meta.json"

        if not self.manifest_file.is_file():
            self.database_directory.mkdir(parents=True, exist_ok=True)
            with self.manifest_file.open("w", encoding="utf-8") as file:
                json.dump({ "tables": [] }, file, indent=2)

        with open(self.manifest_file, "r", encoding="utf-8") as file:
            tables = json.load(file)
            for table in tables["tables"]:
                self._load_table(table)

    def create_table(self, table_name: str):
        """Method to create the table"""
        self.tables[table_name] = []

        with open(self.manifest_file, "r", encoding="utf-8") as file:
            metadata = json.load(file)

        metadata["tables"].append(table_name)
        with open(self.manifest_file, "w", encoding="utf-8") as file:
            json.dump(metadata, file, indent=2)

    def insert_row(self, table_name: str, row_data: list):
        """Method to insert a row to the table"""
        for row in row_data:
            self.tables[table_name].append(row)

        self._save_table(table_name)

    def select_all(self, table_name: str):
        """Method to get all the table data"""
        print(self.tables[table_name])

    def update_row(self, table_name, id, new_row_data):
        """Method to update the row of a table"""
        rows = self.tables[table_name]
        for i, row in enumerate(rows):
            if row["id"] != id:
                continue

            rows[i] = new_row_data

        self._save_table(table_name)

    def _save_table(self, table_name: str):
        """Method to persist the table"""
        file_name = self.database_directory / (table_name + ".json")
        with open(file_name, "w", encoding="utf-8") as file:
            table_data = self.tables[table_name]
            json.dump(table_data, file, indent=2)

    def _load_table(self, table_name: str):
        """Method to load the table into memory"""
        file_name = self.database_directory / (table_name + ".json")
        if not file_name.is_file():
            self.database_directory.mkdir(parents=True, exist_ok=True)
            with file_name.open("w", encoding="utf-8") as file:
                json.dump({}, file, indent=2)

        with open(file_name, "r", encoding="utf-8") as file:
            self.tables[table_name] = json.load(file)
