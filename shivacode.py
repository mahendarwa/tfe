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
    print("✅ Connected to SQL Server")

    # View SQL Server version
    cursor.execute("SELECT @@version;")
    row = cursor.fetchone()
    print(f"SQL Server version: {row[0]}")

    # 🔍 Query to view some rows from dbo.Export_CIOX
    query_sql = """
        SELECT TOP 5 ProjectName, ReportingPopulation, MemberID 
        FROM dbo.Export_CIOX;
    """
    cursor.execute(query_sql)
    results = cursor.fetchall()

    if results:
        print("🔎 Sample rows from Export_CIOX:")
        for r in results:
            print(r)
    else:
        print("No data found in Export_CIOX.")

except pyodbc.Error as ex:
    print(ex)
    sqlstate = ex.args[0]
    if sqlstate == '28000':
        print("❌ Invalid credentials")
    else:
        print("❌ Connection error:", ex)

finally:
    if connection:
        cursor.close()
        connection.close()
        print("✅ Connection closed")
