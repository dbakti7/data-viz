import http.client
import json
import sqlite3

def getPostalCode(lat, lng):
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

def getArea(lat, lng):
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

def populateAreaDB():
    db = sqlite3.connect("taxi.db")
    c = db.cursor()
    for i in range(120, 150):
        for j in range(10350, 10400):
            area = getArea(i/100, j/100)
            if(area == ""):
                continue
            print(i, j, area)
            c.execute("INSERT INTO area VALUES(?,?,?)", (i/100, j/100, area))
    db.commit()
    db.close()

def getAreasFromDB(c):
    areas = []
    for row in c.execute("Select * FROM area"):
        areas.append(row)
    return areas

def getArea(areas, lat, lng):
    ans = ""

    currentMin = 2000000000
    for area in areas:
        temp = abs(lat - area[0]) + abs(lng - area[1])
        if(temp < currentMin):
            currentMin = temp
            ans = area[2]
    return ans
        
#populateAreaDB()

    
db = sqlite3.connect("taxi.db")
c = db.cursor()

areaList = getAreasFromDB(c)
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
        areas = dict()
        for coord in coords:
            area = getArea(areaList, coord[1], coord[0])
            if area != "":
                if(area in areas):
                    areas[area] += 1
                else:
                    areas[area] = 1
        for area in areas:
            c.execute("INSERT INTO taxi VALUES(?,?,?,?,?,?)", (date, hour, minute, second, areas[area], area))
db.commit()
db.close()
