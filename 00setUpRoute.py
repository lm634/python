### CHEAPEST TRAIN ROUTE SCRIPT ###
# script to set up and find cheapest tickets along
# a given train route 
### ------------------------------------------ ###


### set-up
def alert(alertText):
    print(">>> "+alertText+"...")

def warning(alertText):
    print("!!! "+alertText+"...")

def lb():
    print("")


### other lists and variables
journey = []
routeList = []
codeOrder = []
statAndCode = []
info = []
tempErr = 0
progCount = 1
dd = ''
dh = ''
dm = ''
form = ''
browser = ''
lb()
counter=0


###import libraries
try:
    import numpy
    import urllib3
    from robobrowser import RoboBrowser
    from requests.exceptions import ConnectionError
    from bs4 import BeautifulSoup as bs
    import lxml
    from datetime import datetime
    import csv
    import os
    import re
except ImportError:
    tempErr+=1
if tempErr == 0:
    alert('libraries imported')
else:
    warning('there was an error loading libraries')
    alert('ending programme')
    quit()


### working directory
cwd = os.getcwd()
savePath = cwd+'/.../Pytexts/trainBooker/'
if not os.path.exists(savePath):
    os.makedirs(savePath)
    savePath = os.chdir(savePath)
else:
    os.chdir(savePath)
if not os.path.exists(savePath+"savedRoutes/"):
    os.makedirs(savePath+"savedRoutes/")
cwd = os.getcwd()
alert("directory established at "+cwd)


### define functions here
alert("defining functions")


#function that sets up the station list csv file in the directory
def statDownload():
    alert("downloading station list")
    tempURL = 'http://www.nationalrail.co.uk/static/documents/content/station_codes.csv'
    try:
        http = urllib3.PoolManager()
        tempResponse = http.request('GET',tempURL)
        with open('station_codes.csv', 'wb') as f:
            f.write(tempResponse.data)
        tempResponse.release_conn()
    except urllib3.exceptions.MaxRetryError:
        warning("programme requires internet connection")
        quitornot = input("!!! press 'q' to quit or any other key to continue...")
        if quitornot == 'q':
            alert("ending programme")
            quit()
        else:
            input("\n>>> warning!!! if you do not have internet connection, this script will crash... Press enter to continue: ")
    stationNames = []
    stationAbbrv = []
    with open('station_codes.csv') as f:
        csvID = csv.reader(f)
        for row in csvID:
            if ((row[0]!='') and (row[1]!='')) == True:
                stationNames.append(row[0])
                stationAbbrv.append(row[1])
    stationDict = []
    for i in range(len(stationNames)):
        stationDict.append([stationNames[i],stationAbbrv[i]])
    alert("station list loaded")
    lb()


#function in set-up that defines outbound station on text input
def outbound():
    tempStat = 0
    while True:
        jOut = input("outbound station: ")
        for row in stationDict:
            if row[0] == jOut:
                tempStat+=1
                journey.append(row[0])
        if tempStat != 1:
            warning("outbound station not found, please try again")
        elif tempStat == 1:
            break


#function in set-up that defines inbound station on text input
def inbound():
    tempStat = 0
    while True:
        jEnd = input("inbound station: ")
        for row in stationDict:
            if row[0] == jEnd:
                tempStat+=1
                journey.append(row[0])
        if tempStat != 1:
            warning("inbound station not found, please try again")
            print("outbound station: "+journey[0])
        elif tempStat == 1:
            break
            
            
#function that allows station input, or commences loading from the library
def loadStations():
    global journey
    tempIn = input("\n>>> if you wish to load a route from your library, please type 'load', else press the 'enter' key...\n")
    if tempIn == 'load':
        loadRoute()
    else:
        outbound()
        inbound()
        routeList.append(journey[0])
        lb()
        print(">>> your journey is from "+journey[0]+" to "+journey[1]+"...")
        tempStat = 0
        while True:
            nxtStat = input("\n>>> please input the next intermediary station on the route...\n")
            for row in stationDict:
                if row[0] == nxtStat:
                    tempStat+=1
            if tempStat == 1 or nxtStat == '':
                break  
            elif tempStat != 1:
                warning("station not found, please try again") 
        while True:
            routeList.append(nxtStat)
            alert("your journey is between the following stations")
            print(routeList, journey[1])
            tempStat = 0
            while True:
                nxtStat = input("\n>>> please input the next intermediary station on the route, or press the 'enter' key to finalise...\n")
                for row in stationDict:
                    if row[0] == nxtStat:
                        tempStat+=1
                if tempStat == 1 or nxtStat == '':
                    break
                elif tempStat != 1:
                    warning("station not found, please try again")
            if nxtStat == '':
                break
        routeList.append(journey[1])
        alert("your journey is between the following stations: ")
        print(routeList)
        
### ------------------------------------------ ###
##    NOT READY YET
#
#         codeFinder()
#         print(codeOrder)
#         saveFile = input(">>> please type a file name to save the route: ")
#         newCSV = open('savedRoutes/'+saveFile+'.csv', 'wb')
# #        for item in routeList:
# #            newCSV.write(item)
# #            newCSV.write("\n")
#         newCSV.writerow([routeList,codeOrder])
# #        for item in codeOrder:
# #            newCSV.write(item)
# #            newCSV.write("\n")
#         newCSV.close()
#         lb()
### ------------------------------------------ ###

        alert("route saved to library")
    alert("route loaded")
    lb()


#function that runs from within loadStations(), which loads directly from the library dirs
def loadRoute():
    route = input("\n>>> please type in the file name of your saved route here: \n")
    with open(savePath+"savedRoutes/"+route+".csv") as f:
        csvReader = csv.reader(f)
        for row in csvReader:
            routeList.append(row)
    alert("route loading for: ")
    for item in routeList:
        print(item)


#lookup function that appends the station code onto the loader dictionary       
def codeFinder():
    for i in routeList:
        for row in stationDict:
            if row[0] == i:
                codeOrder.append(row[1])
    statAndCode = (routeList,codeOrder)
    print(statAndCode)


#function that determines date and time of travel
def timeOfTravel():
    global dd
    global dh
    global dm
    dd = str(input("Please type the date of your travel here: (dd/mm/yyyy)\n"))
    dh = str(input("\nPlease type the hour you will be travelling here: (24hr)\n"))
    dm = str(input("\nPlease type the approximate minute you will be travelling here: (00,15,30,45)\n"))
    alert('date and time of travel loaded')


#function that sets up the browser and builds the matrix template
def browserSetup():
    global form
    global browser
    alert("setting up browser")
    matrix = [[None]*(len(routeList))]*(len(routeList))
    browser = RoboBrowser(history=True, parser="lxml")
    try:
        browser.open("http://ojp.nationalrail.co.uk/service/planjourney/search")
        form = browser.get_form(action="/service/planjourney/plan")
    except ConnectionError:
        warning("could not access journey details")
        quitornot = input("!!! press 'q' to quit or any other key to continue...")
        if quitornot == 'q':
            alert("ending programme")
            quit()
        else:
            input("\n>>> warning!!! if you do not have internet connection, this script will not run... Press any enter to continue: ")


#function that fills out the form
def formFill(outbound,inbound,date,hour,minute):
    form["from.searchTerm"].value = outbound                            # outgoing station
    form["to.searchTerm"].value = inbound                               # arrival station
    form["timeOfOutwardJourney.monthDay"].value = date                  # date
    form["timeOfOutwardJourney.hour"].value = hour                      # hour
    form["timeOfOutwardJourney.minute"].value = minute                  # minute
    form["_firstClass"].value = "off"                                   # no first class tickets
    form["_standardClass"].value = "on"                                 # standard class
    form["_checkbox"].value = "on"                                      # return ticket?
    #form["timeOfOutwardJourney.arrivalOrDeparture"].value = "DEPART"   # outward arrive/depart
    #form["timeOfReturnJourney.arrivalOrDeparture"].value = ""          #
    #form["timeOfReturnJourney.monthDay"].value = ""                    #
    #form["timeOfReturnJourney.hour"].value = ""                        #
    #form["timeOfReturnJourney.minute"].value = ""                      #
    #form["numberOfAdults"].value = ""                                  #
    #form["firstClass"].value = ['false']                               #
    #form["standardClass"].value = ['true']                             #
    browser.submit_form(form)
    htmltext = bs((str(browser.parsed)),"lxml")
    journeyDts(htmltext)


#function that accesses the fare and journey breakdown
def journeyDts(html):
    global info
    farebd = html.find_all(class_="fare-breakdown")
    spanID = 'type="hidden" value=(.+?)/>'
    regex = (spanID)
    pattern = re.compile(regex)
    price = pattern.findall(str(farebd))
    for line in price:
        info = []
        line = line.replace("1st", "First")
        pattern = re.findall(r'\d+', line)
        info.append([float(''.join([pattern[1],'.',pattern[2]])),None])
### ------------------------------------------ ###
##    NOT READY YET
#     ###Times###
#     journeybd = html.find_all(class_="journey-breakdown")
#     spanID = 'type="hidden" value="(.+?)13|0|GREEN_TICK||"/>'
#     regex = (spanID)
#     pattern = re.compile(regex)
#     journeyTime = pattern.findall(str(journeybd))
#     z = 0
#     for line in journeyTime:
#         if line != '':
#             info[z][1] = (line)
#             z+=1
#     print(info)
### ------------------------------------------ ###


#function acting as a progress counter
def progress(rlength):
    global progCount
    n = rlength - 1
    incr = int(100/(n*(n+1)/2))
    print(progCount*incr,'% complete...')
    progCount+=1


#function creating and filling the matrix to be used for Djikstra's Algorithm
def fillMatrix():
    global info
    length = len(routeList)   
    x = 0
    y = 1
    lb()
    alert('gathering route data')
    while x!=length and y!=length:
        progress(len(routeList))
        formFill(routeList[x][0],routeList[y][0],dd,dh,dm)
        matrix[x][y]=info[0][0]
        y+=1
        if y==length:
            x+=1
            y=x+1        
    print('100 % complete...')
    

#function that sums the values sent by dijkstra function
def sum(list):
    global runningTotal
    runningTotal = 0
    for item in list:
        runningTotal = runningTotal+item
        
        
#function that runs dijkstra's algorithm on the matrix
def dijkstra(finMatrix):
    global runningTotal
    totals = []
    runningTotal = 0
    x = []
    temp = 0
    for item in range(len(finMatrix[0])):
        x.append(temp)
        temp+=1
    y = [0]
    low = 9999999
    for item in finMatrix[0]:
        if item == None:
            number = 0
        else:
            number = item
        totals.append([number,0])
    for i in range(len(x)):
        if i not in y:
            if (totals[i][0]) < low:
                low = i
    y.append(low)
    low = 9999999
    while len(y) < len(x):
        for i in range(len(x)):
            yLen = len(y)-1
            if i not in y and finMatrix[yLen][i] != None and finMatrix[yLen][i] < 9999999:
                loL = 1
                global hist
                hist = []
                hist.append(finMatrix[yLen][i])
                newX = totals[yLen][1]
                newY = yLen
                while True:
                    prevStep = finMatrix[newX][newY]
                    hist.append(prevStep)
                    loL+=1
                    newY = newX
                    newX = totals[newX][1]
                    if (loL) >= (yLen) or ((newY==0)and(newX==0))==True:
                        break
                sum(hist)
                if runningTotal < totals[i][0]:
                    totals[i] = [runningTotal,(len(y)-1)]
                runningTotal = 0
        for i in range(len(x)):
	        if i not in y:
	    	    if (totals[i][0]) < low:
	    		    low = totals[i][0]
	    		    coord = i
        y.append(coord)
        low = 9999999
    routeInfo(matrix,totals,y)
    lb()
    

#function printing back the results from dijkstra function
def routeInfo(finMatrix,finTotals,yVals):
    global counter
    alert('data compiled, printing route information')
    lb()
    lb()
    print('Cambridge to...\n\n')
    for i in range(len(routeList)):
        if i>0:
            print(routeList[i][0],'- advertised price: £',"{0:.2f}".format(matrix[0][i]))
            if matrix[0][i] > finTotals[i][0]:
                print('>>> new price: £',"{0:.2f}".format(finTotals[i][0],'...'))
                difference = "{0:.2f}".format(matrix[0][i] - finTotals[i][0])
                print('!!! saving of: £',difference,'by splitting your route from...')
                x = finTotals[i][1]
                preVert = []
                preVert.append(i)
                preVert.append(x)
                while True:
                    y = x
                    x = finTotals[x][1]
                    preVert.append(y)
                    preVert.append(x)
                    if x == 0:
                        break
                n = len(preVert)-1
                while True:
                    print(routeList[(preVert[n])][0],'==>',routeList[(preVert[n-1])][0])
                    n-=2
                    if n < 1:
                        break
            lb()
    

#testing function that saves a file from the compiler (assign: global counter, counter+=1)
def testSave(name,file,type):
    saveFile = name
    newFile = open('testDirs/'+name+'.'+type,'w')
    newFile.write(file)
    newFile.close()


### __main__ ###
alert("functions defined")
alert("running script")
statDownload()
loadStations()
timeOfTravel()
matrix = [[None]*(len(routeList)) for n in range(len(routeList))]
browserSetup()
fillMatrix()
dijkstra(matrix)
alert("script ran successfully")
lb()
lb()
lb()
