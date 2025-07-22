import pyodbc

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


sql_file_path = "query.sql"  # You can update this file each deployment

try:
    with open(sql_file_path, 'r') as file:
        sql_query = file.read()

    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()
    print("✅ Connected to SQL Server")

    cursor.execute(sql_query)
    result = cursor.fetchall()

    for row in result:
        print(row)

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
