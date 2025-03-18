import pyodbc
import os

print("Connecting to SQL Server...")

# Fetch credentials securely from environment variables
username = os.getenv('USERNAME')  # Should be: Internal\c8x6k9
password = os.getenv('PASSWORDSQL')  # Should be: Dev2s@mpath

# Properly escape backslash in username
escaped_username = username.replace("\\", "\\\\")

connection_string = (
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER=HSTNCMSRDIDEV01.healthspring.inside;"
    f"UID={escaped_username};"
    f"PWD={password};"
    f"Trusted_Connection=no;"
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
