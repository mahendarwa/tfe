import pyodbc

# Connection string
connection_string = (
    r'DRIVER={ODBC Driver 18 for SQL Server};'
    r'SERVER=HSTNCMSRDIQA02.healthspring.inside;'
    r'Trusted_connection=yes;'
    r'TrustServerCertificate=yes;'
    r'DATABASE=Staging;'
    r'DOMAIN=INTERNAL;'
    r'UID=C8X6K9;'
    r'PWD=Dev2s@mpath;'
)

# Establish connection
try:
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()
    print("Connected to SQL Server")

    # Example: Execute a query
    cursor.execute("SELECT @@version;")
    row = cursor.fetchone()
    print(f"SQL Server version: {row[0]}")

    # Execute your SQL update command
    update_sql = """
        UPDATE build.dbo.ProcedureCodeDim 
        SET ProcedureTypeCode = 'H' 
        WHERE procedurecode = 'G0432' AND SourceDataKey = 2;
    """
    cursor.execute(update_sql)
    connection.commit()
    print("✅ SQL update executed successfully")

except pyodbc.Error as ex:
    print(ex)
    sqlstate = ex.args[0]
    if sqlstate == '28000':
        print("Invalid credentials")
    else:
        print("Connection error:", ex)

finally:
    if connection:
        cursor.close()
        connection.close()
        print("Connection closed")
