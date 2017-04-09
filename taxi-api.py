import http.client
import json
import sqlite3

db = sqlite3.connect("taxi.db")
c = db.cursor()

conn = http.client.HTTPSConnection("api.data.gov.sg")

payload = ""

headers = { 'api-key': "eSP8hew3DJNjC0sErarllnOiq3ol2QKY" }

for x in range(0, 25):
    hour = "0" + str(x) if x < 10 else str(x) #must be in two-digit format
    minute = "00"
    second = "00"
    dateTime = date + "T" + hour + "%3A" + minute + "%3A" + second
    conn.request("GET", "/v1/transport/taxi-availability?date_time=" + dateTime, payload, headers)

    res = conn.getresponse()
    data = res.read()

    data = json.loads(data.decode("utf-8"))
    print("Time: " + date + " " + hour + ":" + minute + ":" + second)
    availability = len(data["features"][0]["geometry"]["coordinates"])
    print("Number of available taxis: " + str(availability))

    c.execute("INSERT INTO taxi VALUES(?,?,?,?,?)", (date, hour, minute, second, availability))
db.commit()
db.close()
