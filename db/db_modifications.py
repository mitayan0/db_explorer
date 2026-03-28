import sqlite3 as sqlite
import datetime
import keyring
from db.db_connections import DB_FILE

KEYRING_SERVICE = "DB_Explorer_Credentials"

def add_connection_group(name, parent_id):
    with sqlite.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute(
            "INSERT INTO usf_connection_groups (name, connection_type_id) VALUES (?, ?)", (name, parent_id))
        conn.commit()

def add_connection(data, connection_group_id):
    # Extract password to store only in keyring
    password = data.get("password", "")
    data["password"] = "[SECURE_STORAGE]" # Placeholder in DB

    with sqlite.connect(DB_FILE) as conn:
        c = conn.cursor()

        # -------- SQLite / CSV --------
        if data.get("db_path"):
            c.execute(
                """
                INSERT INTO usf_connections
                (name, short_name, connection_group_id, db_path)
                VALUES (?, ?, ?, ?)
                """,
                (
                    data.get("name"),
                    data.get("short_name"),
                    connection_group_id,
                    data.get("db_path"),
                )
            )

        # -------- ServiceNow --------
        elif data.get("instance_url"):
            c.execute(
                """
                INSERT INTO usf_connections
                (name, short_name, connection_group_id, instance_url, "user", password)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    data.get("name"),
                    data.get("short_name"),
                    connection_group_id,
                    data.get("instance_url"),
                    data.get("user"),
                    data.get("password"),
                )
            )

        # -------- Postgres / Oracle --------
        else:
            c.execute(
                """
                INSERT INTO usf_connections
                (name, short_name, connection_group_id, host, "database", "user", password, port)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    data.get("name"),
                    data.get("short_name"),
                    connection_group_id,
                    data.get("host"),
                    data.get("database"),
                    data.get("user"),
                    data.get("password"),
                    data.get("port"),
                )
            )

        conn.commit()
        conn_id = c.lastrowid
        
        # Save password to system keyring
        if password and conn_id:
            try:
                keyring.set_password(KEYRING_SERVICE, str(conn_id), password)
            except Exception as e:
                print(f"Keyring save error: {e}")

def update_connection(data):
    # Extract password to store only in keyring
    password = data.get("password", "")
    conn_id = data.get("id")
    
    # If a new password is provided, update keyring
    if password and conn_id:
        try:
            keyring.set_password(KEYRING_SERVICE, str(conn_id), password)
        except Exception as e:
            print(f"Keyring update error: {e}")
        data["password"] = "[SECURE_STORAGE]"
    elif conn_id:
        # Keep existing placeholder if no new password
        data["password"] = "[SECURE_STORAGE]"

    with sqlite.connect(DB_FILE) as conn:
        c = conn.cursor()

        # -------- SQLite / CSV --------
        if data.get("db_path"):
            c.execute(
                """
                UPDATE usf_connections
                SET name = ?, short_name = ?, db_path = ?
                WHERE id = ?
                """,
                (
                    data.get("name"),
                    data.get("short_name"),
                    data.get("db_path"),
                    data.get("id")
                )
            )

        # -------- ServiceNow --------
        elif data.get("instance_url"):
            c.execute(
                """
                UPDATE usf_connections
                SET name = ?, short_name = ?, instance_url = ?, "user" = ?, password = ?
                WHERE id = ?
                """,
                (
                    data.get("name"),
                    data.get("short_name"),
                    data.get("instance_url"),
                    data.get("user"),
                    data.get("password"),
                    data.get("id")
                )
            )

        # -------- Postgres / Oracle --------
        else:
            c.execute(
                """
                UPDATE usf_connections
                SET name = ?, short_name = ?, host = ?, "database" = ?, "user" = ?, password = ?, port = ?
                WHERE id = ?
                """,
                (
                    data.get("name"),
                    data.get("short_name"),
                    data.get("host"),
                    data.get("database"),
                    data.get("user"),
                    data.get("password"),
                    data.get("port"),
                    data.get("id")
                )
            )

        conn.commit()

def delete_connection(connection_id):
    with sqlite.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("DELETE FROM usf_connections WHERE id = ?", (connection_id,))
        c.execute(
            "DELETE FROM usf_query_history WHERE connection_id = ?", (connection_id,))
        conn.commit()
    
    # Clean up password from keyring
    try:
        keyring.delete_password(KEYRING_SERVICE, str(connection_id))
    except keyring.errors.PasswordDeleteError:
        pass # Already gone or never existed
    except Exception as e:
        print(f"Keyring delete error: {e}")

def save_query_history(conn_id, query, status, rows, duration):
    with sqlite.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("""
            INSERT INTO usf_query_history 
            (connection_id, query_text, status, rows_affected, execution_time_sec, timestamp) 
            VALUES (?, ?, ?, ?, ?, ?)""",
                  (conn_id, query, status, rows, duration, datetime.datetime.now().isoformat()))
        conn.commit()

def get_query_history(conn_id):
    with sqlite.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("""
            SELECT id, query_text, timestamp, status, rows_affected, execution_time_sec 
            FROM usf_query_history WHERE connection_id = ? ORDER BY timestamp DESC""",
                  (conn_id,))
        return c.fetchall()

def delete_history(history_id):
    with sqlite.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("DELETE FROM usf_query_history WHERE id = ?", (history_id,))
        conn.commit()

def delete_all_history(conn_id):
    with sqlite.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("DELETE FROM usf_query_history WHERE connection_id = ?", (conn_id,))
        conn.commit()

def add_connection_type(name, code):
    with sqlite.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("INSERT INTO usf_connection_types (name, code) VALUES (?, ?)", (name, code))
        conn.commit()

def update_connection_group(group_id, name):
    with sqlite.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("UPDATE usf_connection_groups SET name = ? WHERE id = ?", (name, group_id))
        conn.commit()

def delete_connection_group(group_id):
    with sqlite.connect(DB_FILE) as conn:
        c = conn.cursor()
        # Delete connections within the group first
        c.execute("SELECT id FROM usf_connections WHERE connection_group_id = ?", (group_id,))
        conn_ids = [row[0] for row in c.fetchall()]
        for conn_id in conn_ids:
            delete_connection(conn_id)
        
        c.execute("DELETE FROM usf_connection_groups WHERE id = ?", (group_id,))
        conn.commit()

def update_connection_type(type_id, name, code):
    with sqlite.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("UPDATE usf_connection_types SET name = ?, code = ? WHERE id = ?", (name, code, type_id))
        conn.commit()

def delete_connection_type(type_id):
    with sqlite.connect(DB_FILE) as conn:
        c = conn.cursor()
        # Delete groups within the type first
        c.execute("SELECT id FROM usf_connection_groups WHERE connection_type_id = ?", (type_id,))
        group_ids = [row[0] for row in c.fetchall()]
        for group_id in group_ids:
            delete_connection_group(group_id)
            
        c.execute("DELETE FROM usf_connection_types WHERE id = ?", (type_id,))
        conn.commit()
