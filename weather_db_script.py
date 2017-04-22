import sqlite3

db = sqlite3.connect("taxi.db")
c = db.cursor()
c.execute('''CREATE TABLE taxi_weather
             (day text,
             date text,
             hour text,
             forecast text,
             availability int
             )''')
db.commit()
db.close()
