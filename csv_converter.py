import csv
import xlwt
results = []

with open('public-transport-utilisation-average-public-transport-ridership.csv', 'rt') as file:
    r = csv.reader(file, delimiter=',')
    rows = []
    
    for row in r:
        rows.append(row)
        
    results = rows[1:]

book = xlwt.Workbook()
sh = book.add_sheet("Average Ridership")
row = 0
currentYear = ""
for result in results:
    col = 0
    if result[0] != currentYear:
        currentYear = result[0]
        row += 1
        sh.write(row, 0, int(currentYear))
    if result[1] == "MRT":
        sh.write(row, 1, int(result[2]))
    elif result[1] == "LRT":
        sh.write(row, 2, int(result[2]))
    elif result[1] == "Bus":
        sh.write(row, 3, int(result[2]))
    elif result[1] == "Taxi":
        sh.write(row, 4, int(result[2]))

book.save("Average_ridership.xls")
    


##with open('public-transport-capacity-monthly-taxi-population.csv', 'rt') as file:
##    r = csv.reader(file, delimiter=',')
##    rows = []
##    
##    for row in r:
##        rows.append(row)
##        
##    total = 0
##    currentPeriod = rows[1][0]
##    for row in rows[1:]:
##        if(row[0] != currentPeriod):
##            results.append([currentPeriod, currentPeriod[:4], currentPeriod[5:], total])
##            currentPeriod = row[0]
##            total = 0
##        total += int(row[2])
##        
##
##book = xlwt.Workbook()
##sh = book.add_sheet("Monthly Taxi")
##row = 0
##for result in results:
##    col = 0
##    for data in result:
##        if col == 1 or col == 2:
##            sh.write(row, col, int(data))
##        else:
##            sh.write(row, col, data)
##        col += 1
##    row += 1
##
##book.save("Monthly_Taxi_Population.xls")
##    
