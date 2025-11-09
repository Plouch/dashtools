"""
Database management module supporting both SQLite and PostgreSQL.
"""
import os
from typing import List, Dict, Any, Optional, Tuple
from abc import ABC, abstractmethod

# Determine database type
DATABASE_TYPE = os.getenv('DATABASE_TYPE', 'sqlite').lower()

if DATABASE_TYPE == 'postgresql':
    import psycopg2
    from psycopg2.extras import RealDictCursor
    USE_POSTGRESQL = True
else:
    import sqlite3
    USE_POSTGRESQL = False


class DatabaseAdapter(ABC):
    """Abstract base class for database adapters."""
    
    @abstractmethod
    def get_connection(self):
        pass
    
    @abstractmethod
    def get_tables(self) -> List[str]:
        pass
    
    @abstractmethod
    def get_table_schema(self, table_name: str) -> List[Dict[str, Any]]:
        pass
    
    @abstractmethod
    def create_table(self, table_name: str, columns: List[Dict[str, str]]) -> Tuple[bool, Optional[str]]:
        pass
    
    @abstractmethod
    def drop_table(self, table_name: str) -> bool:
        pass
    
    @abstractmethod
    def add_column(self, table_name: str, column_name: str, column_type: str, default_value: Optional[str] = None) -> bool:
        pass
    
    @abstractmethod
    def get_table_data(self, table_name: str, limit: int = 100, offset: int = 0) -> Tuple[List[Dict[str, Any]], int]:
        pass
    
    @abstractmethod
    def insert_row(self, table_name: str, data: Dict[str, Any]) -> bool:
        pass
    
    @abstractmethod
    def update_row(self, table_name: str, row_id: int, data: Dict[str, Any], id_column: str = 'id') -> bool:
        pass
    
    @abstractmethod
    def delete_row(self, table_name: str, row_id: int, id_column: str = 'id') -> bool:
        pass
    
    @abstractmethod
    def execute_query(self, query: str) -> Tuple[Optional[List[Dict[str, Any]]], Optional[str]]:
        pass


class SQLiteAdapter(DatabaseAdapter):
    """SQLite database adapter."""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
    
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def get_tables(self) -> List[str]:
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            return [row[0] for row in cursor.fetchall()]
        finally:
            conn.close()
    
    def get_table_schema(self, table_name: str) -> List[Dict[str, Any]]:
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = []
            for row in cursor.fetchall():
                columns.append({
                    'cid': row[0],
                    'name': row[1],
                    'type': row[2],
                    'notnull': bool(row[3]),
                    'default_value': row[4],
                    'pk': bool(row[5])
                })
            return columns
        finally:
            conn.close()
    
    def create_table(self, table_name: str, columns: List[Dict[str, str]]) -> Tuple[bool, Optional[str]]:
        if not table_name or not columns:
            return False, 'Table name and at least one column are required'
        
        if not table_name.replace('_', '').replace('$', '').isalnum():
            return False, 'Table name must contain only alphanumeric characters, underscores, or dollar signs'
        
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            column_defs = []
            for col in columns:
                col_name = col.get('name', '').strip()
                col_type = col.get('type', 'TEXT').strip().upper()
                col_pk = col.get('primary_key', False)
                col_notnull = col.get('not_null', False)
                
                if not col_name:
                    continue
                
                if not col_name.replace('_', '').replace('$', '').isalnum():
                    return False, f'Column name "{col_name}" must contain only alphanumeric characters, underscores, or dollar signs'
                
                valid_types = ['TEXT', 'INTEGER', 'REAL', 'BLOB', 'NUMERIC']
                if col_type not in valid_types:
                    return False, f'Invalid column type "{col_type}". Must be one of: {", ".join(valid_types)}'
                
                col_def = f'"{col_name}" {col_type}'
                if col_pk:
                    col_def += " PRIMARY KEY"
                if col_notnull:
                    col_def += " NOT NULL"
                
                column_defs.append(col_def)
            
            if not column_defs:
                return False, 'At least one column with a name is required'
            
            sql = f'CREATE TABLE IF NOT EXISTS "{table_name}" ({", ".join(column_defs)})'
            cursor.execute(sql)
            conn.commit()
            return True, None
        except Exception as e:
            conn.rollback()
            return False, str(e)
        finally:
            conn.close()
    
    def drop_table(self, table_name: str) -> bool:
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            return False
        finally:
            conn.close()
    
    def add_column(self, table_name: str, column_name: str, column_type: str, default_value: Optional[str] = None) -> bool:
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            sql = f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type.upper()}"
            if default_value is not None:
                sql += f" DEFAULT {default_value}"
            cursor.execute(sql)
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            return False
        finally:
            conn.close()
    
    def get_table_data(self, table_name: str, limit: int = 100, offset: int = 0) -> Tuple[List[Dict[str, Any]], int]:
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            total = cursor.fetchone()[0]
            cursor.execute(f"SELECT * FROM {table_name} LIMIT ? OFFSET ?", (limit, offset))
            rows = [dict(row) for row in cursor.fetchall()]
            return rows, total
        finally:
            conn.close()
    
    def insert_row(self, table_name: str, data: Dict[str, Any]) -> bool:
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            columns = ', '.join(data.keys())
            placeholders = ', '.join(['?' for _ in data])
            cursor.execute(f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})", list(data.values()))
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            return False
        finally:
            conn.close()
    
    def update_row(self, table_name: str, row_id: int, data: Dict[str, Any], id_column: str = 'id') -> bool:
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            set_clause = ', '.join([f"{key} = ?" for key in data.keys()])
            cursor.execute(f"UPDATE {table_name} SET {set_clause} WHERE {id_column} = ?", list(data.values()) + [row_id])
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            return False
        finally:
            conn.close()
    
    def delete_row(self, table_name: str, row_id: int, id_column: str = 'id') -> bool:
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM {table_name} WHERE {id_column} = ?", (row_id,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            return False
        finally:
            conn.close()
    
    def execute_query(self, query: str) -> Tuple[Optional[List[Dict[str, Any]]], Optional[str]]:
        if not query.strip().upper().startswith('SELECT'):
            return None, "Only SELECT queries are allowed"
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query)
            return [dict(row) for row in cursor.fetchall()], None
        except Exception as e:
            return None, str(e)
        finally:
            conn.close()


class PostgreSQLAdapter(DatabaseAdapter):
    """PostgreSQL database adapter."""
    
    def __init__(self, host: str, port: int, user: str, password: str, database: str):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
    
    def get_connection(self):
        return psycopg2.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database
        )
    
    def get_tables(self) -> List[str]:
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """)
            return [row[0] for row in cursor.fetchall()]
        finally:
            conn.close()
    
    def get_table_schema(self, table_name: str) -> List[Dict[str, Any]]:
        conn = self.get_connection()
        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("""
                SELECT 
                    ordinal_position as cid,
                    column_name as name,
                    data_type as type,
                    is_nullable = 'NO' as notnull,
                    column_default as default_value,
                    CASE WHEN pk.column_name IS NOT NULL THEN true ELSE false END as pk
                FROM information_schema.columns
                LEFT JOIN (
                    SELECT ku.column_name
                    FROM information_schema.table_constraints tc
                    JOIN information_schema.key_column_usage ku
                        ON tc.constraint_name = ku.constraint_name
                    WHERE tc.constraint_type = 'PRIMARY KEY'
                        AND tc.table_name = %s
                ) pk ON information_schema.columns.column_name = pk.column_name
                WHERE table_name = %s
                ORDER BY ordinal_position
            """, (table_name, table_name))
            return [dict(row) for row in cursor.fetchall()]
        finally:
            conn.close()
    
    def create_table(self, table_name: str, columns: List[Dict[str, str]]) -> Tuple[bool, Optional[str]]:
        if not table_name or not columns:
            return False, 'Table name and at least one column are required'
        
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            column_defs = []
            for col in columns:
                col_name = col.get('name', '').strip()
                col_type = col.get('type', 'TEXT').strip().upper()
                col_pk = col.get('primary_key', False)
                col_notnull = col.get('not_null', False)
                
                if not col_name:
                    continue
                
                # Map SQLite types to PostgreSQL types
                type_map = {
                    'TEXT': 'TEXT',
                    'INTEGER': 'INTEGER',
                    'REAL': 'REAL',
                    'BLOB': 'BYTEA',
                    'NUMERIC': 'NUMERIC'
                }
                pg_type = type_map.get(col_type, 'TEXT')
                
                col_def = f'"{col_name}" {pg_type}'
                if col_pk:
                    col_def += " PRIMARY KEY"
                if col_notnull:
                    col_def += " NOT NULL"
                
                column_defs.append(col_def)
            
            if not column_defs:
                return False, 'At least one column with a name is required'
            
            sql = f'CREATE TABLE IF NOT EXISTS "{table_name}" ({", ".join(column_defs)})'
            cursor.execute(sql)
            conn.commit()
            return True, None
        except Exception as e:
            conn.rollback()
            return False, str(e)
        finally:
            conn.close()
    
    def drop_table(self, table_name: str) -> bool:
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(f'DROP TABLE IF EXISTS "{table_name}"')
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            return False
        finally:
            conn.close()
    
    def add_column(self, table_name: str, column_name: str, column_type: str, default_value: Optional[str] = None) -> bool:
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            type_map = {'TEXT': 'TEXT', 'INTEGER': 'INTEGER', 'REAL': 'REAL', 'BLOB': 'BYTEA', 'NUMERIC': 'NUMERIC'}
            pg_type = type_map.get(column_type.upper(), 'TEXT')
            sql = f'ALTER TABLE "{table_name}" ADD COLUMN "{column_name}" {pg_type}'
            if default_value is not None:
                sql += f" DEFAULT {default_value}"
            cursor.execute(sql)
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            return False
        finally:
            conn.close()
    
    def get_table_data(self, table_name: str, limit: int = 100, offset: int = 0) -> Tuple[List[Dict[str, Any]], int]:
        conn = self.get_connection()
        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(f'SELECT COUNT(*) FROM "{table_name}"')
            total = cursor.fetchone()['count']
            cursor.execute(f'SELECT * FROM "{table_name}" LIMIT %s OFFSET %s', (limit, offset))
            return [dict(row) for row in cursor.fetchall()], total
        finally:
            conn.close()
    
    def insert_row(self, table_name: str, data: Dict[str, Any]) -> bool:
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            columns = ', '.join([f'"{k}"' for k in data.keys()])
            placeholders = ', '.join(['%s' for _ in data])
            cursor.execute(f'INSERT INTO "{table_name}" ({columns}) VALUES ({placeholders})', list(data.values()))
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            return False
        finally:
            conn.close()
    
    def update_row(self, table_name: str, row_id: int, data: Dict[str, Any], id_column: str = 'id') -> bool:
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            set_clause = ', '.join([f'"{key}" = %s' for key in data.keys()])
            cursor.execute(f'UPDATE "{table_name}" SET {set_clause} WHERE "{id_column}" = %s', list(data.values()) + [row_id])
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            return False
        finally:
            conn.close()
    
    def delete_row(self, table_name: str, row_id: int, id_column: str = 'id') -> bool:
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(f'DELETE FROM "{table_name}" WHERE "{id_column}" = %s', (row_id,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            return False
        finally:
            conn.close()
    
    def execute_query(self, query: str) -> Tuple[Optional[List[Dict[str, Any]]], Optional[str]]:
        if not query.strip().upper().startswith('SELECT'):
            return None, "Only SELECT queries are allowed"
        conn = self.get_connection()
        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(query)
            return [dict(row) for row in cursor.fetchall()], None
        except Exception as e:
            return None, str(e)
        finally:
            conn.close()


# Initialize the appropriate database adapter
if USE_POSTGRESQL:
    db_adapter = PostgreSQLAdapter(
        host=os.getenv('POSTGRES_HOST', 'localhost'),
        port=int(os.getenv('POSTGRES_PORT', '5432')),
        user=os.getenv('POSTGRES_USER', 'dashtools'),
        password=os.getenv('POSTGRES_PASSWORD', 'dashtools'),
        database=os.getenv('POSTGRES_DB', 'dashtools')
    )
    print("Using PostgreSQL database")
else:
    DB_PATH = os.getenv('DATABASE_PATH', 'dashtools.db')
    db_adapter = SQLiteAdapter(DB_PATH)
    print(f"Using SQLite database at {DB_PATH}")


# Public API functions that delegate to the adapter
def get_connection():
    """Get a database connection."""
    return db_adapter.get_connection()


def init_database():
    """Initialize the database if it doesn't exist."""
    if not USE_POSTGRESQL:
        if not os.path.exists(DB_PATH):
            conn = get_connection()
            conn.close()
            print(f"Database initialized at {DB_PATH}")
    else:
        # PostgreSQL database should already exist
        try:
            conn = get_connection()
            conn.close()
            print("PostgreSQL database connection successful")
        except Exception as e:
            print(f"Warning: Could not connect to PostgreSQL: {e}")


def get_tables() -> List[str]:
    """Get list of all tables in the database."""
    return db_adapter.get_tables()


def get_table_schema(table_name: str) -> List[Dict[str, Any]]:
    """Get schema information for a table."""
    return db_adapter.get_table_schema(table_name)


def create_table(table_name: str, columns: List[Dict[str, str]]) -> Tuple[bool, Optional[str]]:
    """Create a new table with specified columns."""
    return db_adapter.create_table(table_name, columns)


def drop_table(table_name: str) -> bool:
    """Drop a table."""
    return db_adapter.drop_table(table_name)


def add_column(table_name: str, column_name: str, column_type: str, default_value: Optional[str] = None) -> bool:
    """Add a column to an existing table."""
    return db_adapter.add_column(table_name, column_name, column_type, default_value)


def get_table_data(table_name: str, limit: int = 100, offset: int = 0) -> Tuple[List[Dict[str, Any]], int]:
    """Get data from a table with pagination."""
    return db_adapter.get_table_data(table_name, limit, offset)


def insert_row(table_name: str, data: Dict[str, Any]) -> bool:
    """Insert a row into a table."""
    return db_adapter.insert_row(table_name, data)


def update_row(table_name: str, row_id: int, data: Dict[str, Any], id_column: str = 'id') -> bool:
    """Update a row in a table."""
    return db_adapter.update_row(table_name, row_id, data, id_column)


def delete_row(table_name: str, row_id: int, id_column: str = 'id') -> bool:
    """Delete a row from a table."""
    return db_adapter.delete_row(table_name, row_id, id_column)


def execute_query(query: str) -> Tuple[Optional[List[Dict[str, Any]]], Optional[str]]:
    """Execute a raw SQL query (SELECT only for safety)."""
    return db_adapter.execute_query(query)
