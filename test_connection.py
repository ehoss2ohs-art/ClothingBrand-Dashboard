import pyodbc

server = "البشمهندس"
database = "ClothingBrand"

connection_string = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    f"SERVER={server};"
    f"DATABASE={database};"
    "Trusted_Connection=yes;"
)

connection = pyodbc.connect(connection_string)
cursor = connection.cursor()

cursor.execute("""
    SELECT TABLE_SCHEMA, TABLE_NAME
    FROM INFORMATION_SCHEMA.TABLES
    WHERE TABLE_TYPE = 'BASE TABLE'
    ORDER BY TABLE_NAME
""")

tables = cursor.fetchall()

print("Tables in ClothingBrand:")
for schema, table in tables:
    print(f"\n{schema}.{table}")

    cursor.execute(
        f"SELECT COUNT(*) FROM [{schema}].[{table}]"
    )
    print("Rows:", cursor.fetchone()[0])

cursor.close()
connection.close()