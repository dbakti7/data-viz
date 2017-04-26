import sqlite3

db = sqlite3.connect("taxi.db")
c = db.cursor()
daysNumber = {"07": 31,
              "08": 31,
              "09": 30,
              "10": 31,
              "11": 30,
              "12": 31,
              "01": 31,
              "02": 28,
              "03": 31,
              "04": 15}
months = ["07", "08", "09", "10", "11", "12", "01", "02", "03", "04"]
yearPrefix = "2016-"
days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
day = 5
for month in months:
    if month != "04":
        continue
    if month in ["01", "02", "03", "04"]:
        yearPrefix = "2017-"
    monthPrefix = yearPrefix + month + "-"
    for i in range (1, daysNumber[month] + 1):
        if i < 10:
            date = monthPrefix + "0" + str(i)
        else:
            date = monthPrefix + str(i)

        c.execute("INSERT INTO days VALUES(?,?)", (date, days[day]))
        day = (day + 1) % 7
db.commit()
db.close()
