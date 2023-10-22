import pymysql
import time

conn = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    db='wypiekarnia'
)
cursor = conn.cursor()

cursor.execute("SELECT email, name, surName FROM klijeci")
users = cursor.fetchall()  # Pobierz wszystkie kolumny z wyników
clock = 3
orders_count = {}

for user in users:
    email, name, surName = user  # Wydobywanie danych użytkownika
    cursor.execute("SELECT COUNT(id) FROM zamowienia WHERE email = %s", (email,))
    orders_count[email] = cursor.fetchone()[0]

for i in range(3, 0, -1):
        print(f"Odliczanie: {i}", end='\r')  # Ustawienie end='\r' dla powrotu na początek linii
        time.sleep(1) 

for email, zamowienia in orders_count.items():
     
    name, surName = [user[1:3] for user in users if user[0] == email][0]
    print(f"Imię: {name}, Nazwisko: {surName}, Email: {email}, Liczba zamówień: {zamowienia}")

conn.close()
