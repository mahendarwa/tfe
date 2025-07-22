import pyodbc
import re

# Connection string
connection_string = (
    r'DRIVER={ODBC Driver 18 for SQL Server};'
    r'SERVER=HSTNCMRSRD1QA02.healthspring.inside;'
    r'Trusted_connection=yes;'
    r'TrustServerCertificate=yes;'
    r'DATABASE=Staging;'  
    r'DOMAIN=INTERNAL;'
    r'UID=CBX6K9;'
    r'PWD=Dev3s@mpath;'
)

# SQL file path (change as needed)
sql_file_path = "query.sql"

try:
    # Read and split on GO (case-insensitive, line-start)
    with open(sql_file_path, 'r') as file:
        sql_script = file.read()

    batches = re.split(r'(?i)^\s*GO\s*$', sql_script, flags=re.MULTILINE)

    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()
    print("✅ Connected to SQL Server")

    for batch in batches:
        batch = batch.strip()
        if batch:
            cursor.execute(batch)
            connection.commit()
            print("✅ Executed batch:\n", batch.splitlines()[0]) 

except pyodbc.Error as ex:
    print("❌ pyODBC Error:", ex)
    sqlstate = ex.args[0]
    if sqlstate == '28000':
        print("❌ Invalid credentials")
    else:
        print("❌ Connection error:", ex)

except Exception as e:
    print("❌ General error:", e)

finally:
    if 'cursor' in locals():
        cursor.close()
    if 'connection' in locals():
        connection.close()
        print("✅ Connection closed")
