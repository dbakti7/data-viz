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
    conn = http.client.HTTPSConnection("api.data.gov.sg")
    headers = { 'api-key': "eSP8hew3DJNjC0sErarllnOiq3ol2QKY" }
    conn.request("GET", "/v1/environment/2-hour-weather-forecast?date_time=2016-12-12T09%3A00%3A00", headers=headers)
    res = conn.getresponse()
    data = res.read()
    data = json.loads(data.decode("utf-8"))
    areas = data["area_metadata"]
    for area in areas:
        long = area["label_location"]["longitude"]
        lat = area["label_location"]["latitude"]
        c.execute("INSERT INTO area VALUES(?,?,?)", (lat, long, area["name"]))
    db.commit()
    db.close()

def populateRegionDB():
    db = sqlite3.connect("taxi.db")
    c = db.cursor()
    conn = http.client.HTTPSConnection("api.data.gov.sg")
    headers = { 'api-key': "eSP8hew3DJNjC0sErarllnOiq3ol2QKY" }
    conn.request("GET", "/v1/environment/pm25?date_time=2016-12-12T09%3A00%3A00", headers=headers)
    res = conn.getresponse()
    data = res.read()
    data = json.loads(data.decode("utf-8"))
    areas = data["region_metadata"]
    for area in areas:
        long = area["label_location"]["longitude"]
        lat = area["label_location"]["latitude"]
        c.execute("INSERT INTO region VALUES(?,?,?)", (lat, long, area["name"]))
    db.commit()
    db.close()

def getAreasFromDB(c):
    areas = []
    for row in c.execute("SELECT * FROM area"):
        areas.append(row)
    return areas

def getRegionsFromDB(c):
    regions = []
    for row in c.execute("SELECT * FROM region"):
        regions.append(row)
    print(regions)
    return regions

def getArea(areas, lat, lng):
    ans = ""

    currentMin = 2000000000
    for area in areas:
        temp = abs(lat - area[0]) + abs(lng - area[1])
        if(temp < currentMin):
            currentMin = temp
            ans = area[2]
    return ans

def getAreaCoord(areas, areaName):
    for area in areas:
        if area[2] == areaName:
            return area[:2]
    return ""

def getForecast(dateTime):
    conn = http.client.HTTPSConnection("api.data.gov.sg")
    headers = { 'api-key': "eSP8hew3DJNjC0sErarllnOiq3ol2QKY" }
    conn.request("GET", "/v1/environment/2-hour-weather-forecast?date_time=" + dateTime, headers=headers)
    res = conn.getresponse()
    data = res.read()
    data = json.loads(data.decode("utf-8"))
    items = data["items"]
    if len(items) == 0:
        return ""
    forecasts = items[0]
    if not ("forecasts" in forecasts):
        return ""
    return forecasts["forecasts"]

def getPSIData(dateTime):
    conn = http.client.HTTPSConnection("api.data.gov.sg")
    headers = { 'api-key': "eSP8hew3DJNjC0sErarllnOiq3ol2QKY" }
    conn.request("GET", "/v1/environment/psi?date_time=" + dateTime, headers=headers)
    res = conn.getresponse()
    data = res.read()
    data = json.loads(data.decode("utf-8"))
    items = data["items"]
    if len(items) == 0:
        return ""
    readings = items[0]
    if not ("readings" in readings):
        return ""
    readings = readings["readings"]
    if not ("psi_three_hourly" in readings):
        return ""
    return readings["psi_three_hourly"]

def getPM25Data(dateTime):
    conn = http.client.HTTPSConnection("api.data.gov.sg")
    headers = { 'api-key': "eSP8hew3DJNjC0sErarllnOiq3ol2QKY" }
    conn.request("GET", "/v1/environment/pm25?date_time=" + dateTime, headers=headers)
    res = conn.getresponse()
    data = res.read()
    data = json.loads(data.decode("utf-8"))
    items = data["items"]
    if len(items) == 0:
        return ""
    readings = items[0]
    if not ("readings" in readings):
        return ""
    readings = readings["readings"]
    if not ("pm25_one_hourly" in readings):
        return ""
    return readings["pm25_one_hourly"]

def getWeather(forecasts, dateTime, area):
    for forecast in forecasts:
        if forecast["area"] == area:
            return forecast["forecast"]
    return ""
        
#populateAreaDB()
#populateRegionDB()

db = sqlite3.connect("taxi.db")
c = db.cursor()
getRegionsFromDB(c)
##areaList = getAreasFromDB(c)
##regionList = getRegionsFromDB(c)
##conn = http.client.HTTPSConnection("api.data.gov.sg")
##
##payload = ""
##
##headers = { 'api-key': "eSP8hew3DJNjC0sErarllnOiq3ol2QKY" }
##
##datePrefix = "2017-04-"
##for i in range (1, 16):
##    if i < 10:
##        date = datePrefix + "0" + str(i)
##    else:
##        date = datePrefix + str(i)
##    for x in range(0, 24):
##        hour = "0" + str(x) if x < 10 else str(x) #must be in two-digit format
##        minute = "00"
##        second = "00"
##        dateTime = date + "T" + hour + "%3A" + minute + "%3A" + second
##        conn.request("GET", "/v1/transport/taxi-availability?date_time=" + dateTime, payload, headers)
##
##        res = conn.getresponse()
##        data = res.read()
##
##        data = json.loads(data.decode("utf-8"))
##        print("Time: " + date + " " + hour + ":" + minute + ":" + second)
##        if not("features" in data):
##            continue
##        features = data["features"]
##        if len(features) == 0:
##            continue
##        features = features[0]
##        if not("geometry" in features):
##            continue
##        coords = features["geometry"]
##        if not("coordinates" in coords):
##            continue
##        coords = coords["coordinates"]
##        
##        availability = len(coords)
##        print("Number of available taxis: " + str(availability))
##        
##        if(availability > 0):
##            areas = dict()
##            for coord in coords:
##                area = getArea(areaList, coord[1], coord[0])
##                if area != "":
##                    if(area in areas):
##                        areas[area] += 1
##                    else:
##                        areas[area] = 1
##            forecasts = getForecast(dateTime)
##            PSIData = getPSIData(dateTime)
##            PM25Data = getPM25Data(dateTime)
##            for area in areas:
##                forecast = getWeather(forecasts, dateTime, area)
##                areaCoord = getAreaCoord(areaList, area)
##                region = getArea(regionList, areaCoord[0], areaCoord[1])
##                PSIValue = PSIData[region] if region in PSIData else 0
##                PM25Value = PM25Data[region] if region in PM25Data else 0
##                c.execute("INSERT INTO taxi VALUES(?,?,?,?,?,?,?,?,?,?)", (date, hour, minute, second, areas[area], area, region, forecast, PSIValue, PM25Value))
##    db.commit()
##db.close()
