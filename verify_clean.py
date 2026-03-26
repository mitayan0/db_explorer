import sqlite3

db_path = r'x:\db_explorer\databases\hierarchy.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

tables = ['usf_connections', 'usf_query_history', 'usf_connection_groups']

print('\n--- DB CLEANLINESS REPORT ---')
for table in tables:
    try:
        cursor.execute(f'SELECT count(*) FROM {table}')
        count = cursor.fetchone()[0]
        print(f'Table {table}: {count} rows')
    except Exception as e:
        print(f'Wait, table {table} not found or error: {e}')

conn.close()
