if query_type == "list_tables":
    with open("list_tables.sql", "r") as file:
        sql_query = file.read()

    cursor.execute(sql_query)
    for row in cursor.fetchall():
        print(f"Table: {row.TABLE_SCHEMA}.{row.TABLE_NAME}")
