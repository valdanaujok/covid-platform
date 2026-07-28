from snowflake_connection import create_connection

connection = create_connection()

cursor = connection.cursor()

cursor.execute("""
SELECT CURRENT_USER(),
       CURRENT_DATABASE(),
       CURRENT_SCHEMA(),
       CURRENT_ROLE();
""")

result = cursor.fetchone()

print(result)

cursor.close()
connection.close()