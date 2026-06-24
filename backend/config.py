import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="mysql@password123",
    database="ecommerce"
)

cursor = db.cursor(dictionary=True)