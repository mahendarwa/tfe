import pyodbc
import os

# Build connection string
conn_str = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=HSTNCMSRDIDEV01.healthspring.inside;"
    "DATABASE=master;"
    f"UID={os.getenv('USERNAME')};"
    f"PWD={os.getenv('PASSWORDSQL')};"
    "TrustServerCertificate=yes;"
    "Trusted_Connection=no;"
)

try:
    print("Connecting to SQL Server...")
    conn = pyodbc.connect(conn_str, timeout=5)
    cursor = conn.cursor()
    cursor.execute("SELECT @@VERSION;")
    row = cursor.fetchone()
    print("Connection successful!")
    print(f"SQL Server Version:\n{row[0]}")
except pyodbc.Error as e:
    print("Connection failed:", e)
finally:
    if 'conn' in locals():
        conn.close()
        print("Connection closed.")
