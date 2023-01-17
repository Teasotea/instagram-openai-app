import sqlite3

conn = sqlite3.connect('db.sqlite')
print("Opened database successfully")

conn.execute('CREATE TABLE User (name TEXT, email TEXT,  password TEXT)')
print("Table created successfully")
conn.close()