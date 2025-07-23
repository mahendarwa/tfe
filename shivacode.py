import pyodbc

# Connection string
connection_string = (
    r'DRIVER={ODBC Driver 18 for SQL Server};'
    r'SERVER=HSTNCMRSRDIQA02.healthspring.inside;'
    r'Trusted_connection=yes;'
    r'TrustServerCertificate=yes;'
    r'DATABASE=Plandata_prod;'
    r'DOMAIN=INTERNAL;'
    r'UID=C8X6K9;'
    r'PWD=Dev3s@mpath;'
)

try:
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()
    print("✅ Connected to SQL Server")

    # Read and split the SQL script
    with open("query.sql", "r") as file:
        sql_script = file.read()

    # Split using GO (case-insensitive + strip leading/trailing whitespace)
    commands = [cmd.strip() for cmd in sql_script.split('GO') if cmd.strip()]

    for command in commands:
        cursor.execute(command)
        connection.commit()

    print("✅ SQL script executed successfully")

except Exception as e:
    print(f"❌ Error: {e}")

finally:
    if 'cursor' in locals():
        cursor.close()
    if 'connection' in locals():
        connection.close()
