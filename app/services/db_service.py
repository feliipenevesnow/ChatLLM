from flask_mysqldb import MySQL
from app import mysql

def fetch_insemination_data():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM inseminacao")
    records = cursor.fetchall()
    db_info = "\n".join([f"ID: {row[0]}, Data: {row[1]}, Valor: {row[2]}" for row in records])
    return db_info
