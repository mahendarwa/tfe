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

    # Example: Execute a query to view SQL Server version
    cursor.execute("SELECT @@version;")
    row = cursor.fetchone()
    print(f"SQL Server version: {row[0]}")

    # 🔍 Query to view SourceDataKey for given procedurecode
    query_sql = """
        SELECT SourceDataKey 
        FROM build.dbo.ProcedureCodeDim 
        WHERE procedurecode = 'G0432';
    """
    cursor.execute(query_sql)
    results = cursor.fetchall()

    if results:
        print("🔎 Retrieved SourceDataKey values:")
        for r in results:
            print(f"SourceDataKey: {r[0]}")
    else:
        print("No matching records found.")

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
