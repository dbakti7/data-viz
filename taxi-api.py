import http.client
import json
import sqlite3

def getPostalCode(lng, lat):
    conn = http.client.HTTPConnection("maps.googleapis.com")

    payload = ""

    conn.request("GET", "/maps/api/geocode/json?latlng=" + str(lat) + "," + str(lng), payload)
    res = conn.getresponse()
    data = res.read()
    data = json.loads(data.decode("utf-8"))
    if(len(data["results"]) > 0):
        address = data["results"][0]["address_components"]
        for addr in address:
            if addr["types"][0] == "postal_code":
                return addr["long_name"]
    return ""

def getArea(lng, lat):
    conn = http.client.HTTPConnection("maps.googleapis.com")

    payload = ""

    conn.request("GET", "/maps/api/geocode/json?latlng=" + str(lat) + "," + str(lng), payload)
    res = conn.getresponse()
    data = res.read()
    data = json.loads(data.decode("utf-8"))
    if(len(data["results"]) > 0):
        address = data["results"][0]["address_components"]
        for addr in address:
            if addr["types"][0] == "neighborhood":
                return addr["long_name"]
    return ""



db = sqlite3.connect("taxi.db")
c = db.cursor()

conn = http.client.HTTPSConnection("api.data.gov.sg")

payload = ""

headers = { 'api-key': "eSP8hew3DJNjC0sErarllnOiq3ol2QKY" }

date = "2017-03-15"
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
    coords = data["features"][0]["geometry"]["coordinates"]
    availability = len(coords)
    print("Number of available taxis: " + str(availability))
    if(availability > 0):
        count = 0
        areas = dict()
        for coord in coords:
            count += 1
            if(count == 100):
                break
            area = getArea(data["features"][0]["geometry"]["coordinates"][0][0], data["features"][0]["geometry"]["coordinates"][0][1])
            if area != "":
                if(area in areas):
                    areas[area] += 1
                else:
                    areas[area] = 1
        for area in areas:
            c.execute("INSERT INTO taxi VALUES(?,?,?,?,?,?)", (date, hour, minute, second, areas[area], area))
db.commit()
db.close()
