# -*- coding: utf-8 -*-
import csv
import sqlite3

csv_filepath = 'tokyo2020.csv'
db_filepath = 'db.sqlite3'

# Connect to the DB by creating a Connection object in memory.
db = sqlite3.connect(db_filepath)
# Create a Cursor object (indicating the row to be processed in the DB).
c = db.cursor()

# Load the CSV file and insert the contents into the DB file.
with open(csv_filepath, 'r', encoding="utf-8") as f:
    b = csv.reader(f)
    header = next(b)
    for t in b:
        # Insert data for each row in table.
        c.execute('INSERT INTO records_swimmingresult VALUES (?, ?, ?, ?, ?, ?, ?);', t)

# Reflect the changes in the DB (commit).
db.commit()

# Close the connection to the DB.
db.close()
