import sqlite3

class db_handler:
    def __init__(self):
        self.databases = {}

    def add_query(self, db_name, query_name, query, read_only=False):
        if db_name in self.databases:
            self.databases[db_name].add_query(query_name, Query(query, read_only))

    def execute_premade_query(self, db_name, query_name, permission_level, parameters=None):
        if db_name in self.databases:
            return self.databases[db_name].execute_premade_query_low_level(query_name, permission_level, parameters)

    def add_db(self, db_name, db_file):
        new_db = DataBase(db_name, db_file)
        self.databases[db_name] = new_db

class Query:
    def __init__(self, query, read_only):
        self.query = query
        self.read_only = read_only

class DataBase:
    def __init__(self, db_name, db_file):
        self.name = db_name
        self.path = db_file
        self.permisson_level_read = 99        
        self.permisson_level_write = 99
        self.permisson_level_bespoke = 99
        self.open_connections = []
        self.premade_queries = {}

    def __str__(self):
        permissions_info = f"Read Permission: {self.permisson_level_read}\n" \
                           f"Write Permission: {self.permisson_level_write}\n" \
                           f"Bespoke Permission: {self.permisson_level_bespoke}"

        return f"Database Information:\n" \
               f"Name: {self.name}\n" \
               f"File Path: {self.path}\n" \
               f"Open Connections: {len(self.open_connections)}\n" \
               f"Permissions:\n{permissions_info}"

    def add_query(self, query_name, query):
        """
        Add a pre-made query to the database.

        Parameters:
        - query_name (str): The name to identify the query.
        - query (Query): The SQL query string and permison type.
        """
        self.premade_queries.update({query_name: query})

    def remove_query(self, query_name):
        """
        Remove a pre-made query from the database.

        Parameters:
        - query_name (str): The name of the pre-made query to be removed.
        """
        if query_name in self.premade_queries:
            del self.premade_queries[query_name]
            print(f"Query '{query_name}' removed successfully.")
        else:
            print(f"Error: Query '{query_name}' not found.")


    def set_perms(self, permisson_level_read, permisson_level_write, permisson_level_bespoke):
        """
        Set permission levels for read, write, and bespoke operations.

        Parameters:
        - permisson_level_read (int): Read permission level.
        - permisson_level_write (int): Write permission level.
        - permisson_level_bespoke (int): Bespoke permission level.
        """
        self.permisson_level_read = permisson_level_read
        self.permisson_level_write = permisson_level_write
        self.permisson_level_bespoke = permisson_level_bespoke

    def _open_connection(self):
        """
        Open a connection to the database.

        Returns:
        - sqlite3.Connection: The database connection.
        """
        try:
            connection = sqlite3.connect(f"./databases/{self.path}")
            self.open_connections.append(connection)
            return connection
        except sqlite3.Error as e:
            print(f"Error opening connection: {e}")

    def _close_connection(self, connection):
        """
        Close the given database connection.

        Parameters:
        - connection (sqlite3.Connection): The database connection to close.
        """
        if connection not in self.open_connections:
            print("Connection not valid (may already be closed)")
            return
        try:
            index = self.open_connections.index(connection)
            self.open_connections.pop(index).close()
        except sqlite3.Error as e:
            print(f"Error closing connection: {e}")

    def execute_premade_query_low_level(self, query_name, permission_level=0, parameters=None):
        """
        Execute a pre-made query from the database.

        Parameters:
        - query_name (str): The name of the pre-made query.
        - parameters (tuple or None): Parameters to substitute into the query (optional).

        Returns:
        - list of tuples: Result of the query.
        """
        if query_name not in self.premade_queries:
            print(f"Error: Query '{query_name}' not found.")
            return None

        query = self.premade_queries[query_name]
        if query.read_only:
            if permission_level < self.permisson_level_read:
                print("permission denid")
                return
        else:
            if permission_level < self.permisson_level_write:
                print("permission denid")
                return
    
        query = query.query

        connection = self._open_connection()
        try:
            with connection:
                if parameters:
                    result = connection.execute(query, parameters).fetchall()
                else:
                    result = connection.execute(query).fetchall()
            return result
        except sqlite3.Error as e:
            print(f"Error executing query '{query_name}': {e}")
        finally:
            self._close_connection(connection)