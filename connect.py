import mysql.connector
conn=mysql.connector.connect(host='sql12.freesqldatabase.com',user='sql12777796',password='SktVxwR9Hp',db='sql12777796')
print(conn.connection_id)
cursor=conn.cursor()
cursor.execute("SELECT Value FROM Status WHERE Varname = 'status'")
result = cursor.fetchone()


# to change the entry


# cursor.execute("UPDATE Status SET Value = %s WHERE Varname = %s", (9, 'status'))
# conn.commit()


if result:
    status_value = result[0]
    print(f"Status value: {status_value}")
else:
    print("No status entry found.")

cursor.close()
conn.close()