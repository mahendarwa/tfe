import os
import sys
import pyodbc

connection = None
cursor = None

query_type = sys.argv[1] if len(sys.argv) > 1 else "list_tables"
server = sys.argv[2] if len(sys.argv) > 2 else "HSTNCMSRDIQA02.healthspring.inside"
database = sys.argv[3] if len(sys.argv) > 3 else "Staging"

uid = os.getenv("SQL_UID")
pwd = os.getenv("SQL_PWD")

connection_string = (
    r'DRIVER={ODBC Driver 18 for SQL Server};'
    rf'SERVER={server};'
    rf'DATABASE={database};'
    r'Trusted_Connection=yes;'
    r'DOMAIN=INTERNAL;'
    rf'UID={uid};'
    rf'PWD={pwd};'
    r'TrustServerCertificate=yes;'
)

connection = pyodbc.connect(connection_string)
cursor = connection.cursor()
print(f"Connected to SQL Server:--  {server}")

if query_type == "list_tables":
    with open("sql_cmd.sql", "r") as file:
        sql_query = file.read()
    cursor.execute(sql_query)
    for row in cursor.fetchall():
        print(f"Table: {row.TABLE_SCHEMA}.{row.TABLE_NAME}")

cursor.close()
connection.close()
print("Connection closed")
