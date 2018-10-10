import sqlite3
import os
from scorelib import load
import sys

os.system("sqlite3 scorelib.dat < scorelib.sql")
data = load(sys.argv[1])

conn = sqlite3.connect('scorelib.dat')
conn.text_factory = str

c = conn.cursor()

# store composition authors
for record in data:
    for author in (record.edition.composition.authors):
        checker = False
        for row in c.execute("Select name from person"):
            if author.name == row[0]: checker = True

        if checker == False: c.execute("INSERT INTO person(name, born, died) VALUES  (?, ?, ?)", (author.name, author.born, author.died))
        conn.commit()

# store edition authors
for record in data:
    for author in (record.edition.authors):
        checker = False
        for row in c.execute("Select name from person"):
            if author.name == row[0]: checker = True
        if checker == False: c.execute("INSERT INTO person(name, born, died) VALUES  (?, ?, ?)", (author.name, None, None))
        conn.commit()





for row in c.execute("Select name from person"):
 print (row[0])
