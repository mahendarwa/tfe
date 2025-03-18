import pyodbc

print("Connecting to SQL Server...")

# Correctly formatted raw string username
username = r"INTERNAL\c8x6k9"
password = "Dev2s@mpath"

connection_string = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=HSTNCMSRDIDEV01.healthspring.inside;"
    f"UID={username};"
    f"PWD={password};"
    "Trusted_Connection=no;"
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
    print("Connection failed:", e)
