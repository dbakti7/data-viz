import sqlite3

db = sqlite3.connect("taxi.db")
c = db.cursor()
c.execute('''CREATE TABLE taxi
             (date text,
             hour text,
             minute text,
             second text,
             availability int,
             region text,
             forecast text
             )''')
c.execute('''CREATE TABLE area
             (lat real,
              lng real,
              area text)''')
db.commit()
db.close()
