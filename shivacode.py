import pyodbc

print("Connecting to SQL Server...")

connection_string = (
    r'DRIVER={ODBC Driver 17 for SQL Server};'
    r'SERVER=HSTNCMSRDIDEV01.healthspring.inside;'
    r'Trusted_Connection=no;'
    r'UID=Internal\\c8x6k9;'
    r'PWD=Dev2s@mpath;'
)

try:
    conn = pyodbc.connect(connection_string, timeout=5)
    cursor = conn.cursor()
    cursor.execute("SELECT @@VERSION;")
    row = cursor.fetchone()
    print("Connection successful!")
    print(f"SQL Server version: {row[0]}")
    cursor.close()
    conn.close()
except pyodbc.Error as e:
    print(f"Connection failed: {e}")
