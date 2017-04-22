import sqlite3

def executeQuery(q):
   rows = []
   for row in c.execute(q):
       rows.append(row)
   return rows

def getWeather(c):
    query = "SELECT DISTINCT forecast from taxi"
    return executeQuery(query)

def getTaxiFromWeather(c):
    result = []
    weathers = getWeather(c)
    query = "SELECT day, date, hour, forecast, SUM(availability) as 'total' FROM ( SELECT * FROM Taxi JOIN Days ON Taxi.Date = Days.Date) WHERE ( forecast = '{}') GROUP BY date, hour"
    
    for weather in weathers:
        tmp = query.format(weather[0])
        result.append(executeQuery(tmp))

    return result

db = sqlite3.connect("taxi.db")
c = db.cursor()
result = getTaxiFromWeather(c)

for rows in result:
    for element in rows:
        c.execute("INSERT INTO taxi_weather VALUES(?,?,?,?,?)", (element[0], element[1], element[2], element[3], element[4]))

db.commit()
db.close()
