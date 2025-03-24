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

try:
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()
    print("✅ Connected to SQL Server")

    # 🔍 Check if dbo.Export_CIOX exists
    check_table_query = """
        SELECT 1 
        FROM INFORMATION_SCHEMA.TABLES 
        WHERE TABLE_SCHEMA = 'dbo' AND TABLE_NAME = 'Export_CIOX';
    """
    cursor.execute(check_table_query)
    exists = cursor.fetchone()

    if exists:
        print("✅ Table dbo.Export_CIOX exists in Staging database.")
    else:
        print("❌ Table dbo.Export_CIOX does NOT exist in Staging database.")

except pyodbc.Error as ex:
    print(ex)
    sqlstate = ex.args[0]
    if sqlstate == '28000':
        print("❌ Invalid credentials")
    else:
        print("❌ Connection error:", ex)

finally:
    if 'cursor' in locals():
        cursor.close()
    if 'connection' in locals():
        connection.close()
        print("✅ Connection closed")
