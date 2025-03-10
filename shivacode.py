import pyodbc

# Connection string
connection_string = (
    r'DRIVER={ODBC Driver 18 for SQL Server};'
    r'SERVER=HSTNCMSRDIQA02.healthspring.inside;'
    r'Trusted_connection=yes;'
    r'TrustServerCertificate=yes;'
    r'DATABASE=staging;'
    r'DOMAIN=INTERNAL;'
    r'UID=C8X6K9;'
    r'PWD=Dev2s@mpath;'
)

try:
    # Establish connection
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()
    print("Connected to SQL Server")

    # Execute a test query
    cursor.execute("SELECT @@VERSION;")
    row = cursor.fetchone()
    print(f"SQL Server version: {row[0]}")

except pyodbc.Error as ex:
    print("Connection error:", ex)
    sqlstate = ex.args[0]
    if sqlstate == '28000':
        print("Invalid credentials")

finally:
    if 'cursor' in locals() and cursor:
        cursor.close()
    if 'connection' in locals() and connection:
        connection.close()
        print("Connection closed")
