import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="sakshi2007",   # 👈 YOUR PASSWORD
    database="food_waste"
)

cursor = conn.cursor()