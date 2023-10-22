import pymysql;  

conn = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    db='wypiekarnia'
)
cursor = conn.cursor()

cursor.execute("SELECT * FROM klijeci")
emails = [row[0] for row in cursor.fetchall()]

orders_count = {}

for email in emails:
    cursor.execute("SELECT COUNT(id) FROM zamowienia WHERE email = %s", (email,))
    orders_count[email] = cursor.fetchone()[0]

for email, zamowienia in orders_count.items():
    print(f"Email: {email}, Liczba zamówień: {zamowienia}")

conn.close()
