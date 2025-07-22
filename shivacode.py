import pyodbc
import re

# SQL Server connection string (working one)
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

# Path to your SQL file (update this per deployment)
sql_file_path = "query.sql"

try:
    with open(sql_file_path, 'r') as file:
        sql_script = file.read()

    # Split SQL script into batches on GO
    batches = re.split(r'(?i)^\s*GO\s*$', sql_script, flags=re.MULTILINE)

    connection = pyodbc.connect(connection_string, timeout=10)
    cursor = connection.cursor()
    print("✅ Connected to SQL Server")

    for batch in batches:
        batch = batch.strip()
        if batch:
            try:
                cursor.execute(batch)
                connection.commit()
                print(f"✅ Executed batch:\n{batch.splitlines()[0]}")
            except Exception as exec_err:
                print(f"❌ Error in batch:\n{batch}\n{exec_err}")
                raise

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
