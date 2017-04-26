import sqlite3

db = sqlite3.connect("taxi.db")
c = db.cursor()
c.execute('''CREATE TABLE taxi
             (date text,
             hour text,
             minute text,
             second text,
             availability int,
             area text,
             region text,
             forecast text,
             psi int,
             pm25 int
             )''')

c.execute('''CREATE TABLE area
             (lat real,
              lng real,
              area text)''')

c.execute('''CREATE TABLE region
             (lat real,
              lng real,
              region text)''')

db.commit()
db.close()
