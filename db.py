from database import Database

database = Database(database_name="employees")
database.select_all("roles")
database.select_all("users")
