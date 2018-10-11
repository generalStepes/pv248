import sqlite3
import os
from scorelib import load
import sys

def lookupCompoAuthor(data):
    for author in (data.edition.composition.authors):
        for row in c.execute("Select id from person where name=?", (author.name,)):
            return(row[0])

def storeScoreAuthor(compoID, authorID):
    c.execute("INSERT INTO score_author(score, composer) VALUES  (?, ?)", (compoID, authorID))
    conn.commit()


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


# store composition
for record in data:
    c.execute("INSERT INTO score(name, genre, key, incipit, year) VALUES  (?, ?, ?, ?, ?)", (record.edition.composition.name, record.edition.composition.genre, record.edition.composition.key, record.edition.composition.incipit, record.edition.composition.year))
    conn.commit()
    compoAuthor = lookupCompoAuthor(record)
    for item in (c.execute("Select max(id) from score")):
        compoID = item[0]
    storeScoreAuthor(compoID,compoAuthor)

# store voices
for record in data:
    for index, voice in enumerate(record.edition.composition.voices):
        c.execute("INSERT INTO voice(number, score, range, name) VALUES  (?, ?, ?, ?)", (index+1, compoID, voice.range, voice.name))
        conn.commit()

#for row in c.execute("Select * from voice"):
 #for line in row:
#    print (line)
