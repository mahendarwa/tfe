if query_type == "list_tables":
    with open("sql_cmd.sql", "r") as file:
        sql_query = file.read()
        cursor.execute(sql_query)
        for row in cursor.fetchall():
            print(f"Table: {row.TABLE_SCHEMA}.{row.TABLE_NAME}")

elif query_type == "execute_view_script":
    with open("sql_cmd.sql", "r") as file:
        sql_script = file.read()
        for statement in sql_script.split(";"):
            if statement.strip():
                cursor.execute(statement.strip())
        print("View script executed.")
