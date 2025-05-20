from database import Database

database = Database(database_name="employees")
database.update_row("users", 3, { "id": 3, "name": "Mark", "email": "mark@example.com" })
database.select_all("roles")
database.select_all("users")

