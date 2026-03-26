import sqlite3
import os

db_path = r'x:\db_explorer\databases\hierarchy.db'

try:
    if not os.path.exists(db_path):
        print(f"Error: {db_path} not found.")
        exit(1)
        
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Wipe personal data tables
    tables_to_wipe = ['usf_connections', 'usf_query_history', 'usf_connection_groups', 'usf_processes']
    
    for table in tables_to_wipe:
        try:
            print(f'Wiping {table}...')
            cursor.execute(f'DELETE FROM {table}')
        except sqlite3.OperationalError as e:
            if "no such table" in str(e).lower():
                print(f"Table {table} does not exist. Skipping.")
            else:
                raise e

    conn.commit()
    print('Deep Clean Successful!')
    conn.close()
except Exception as e:
    print(f'Error cleaning DB: {e}')
    exit(1)
