###import
from robobrowser import RoboBrowser
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup as bs
import lxml
import re

def alert(alertText):
    print(">>> "+alertText+"...")

def warning(alertText):
    print("!!! "+alertText+"...")

def lb():
    print("")
    
routeList = ['Oakham','Stamford (Lincs)','Peterborough','March','Ely','Cambridge']
dd = '05/08/2016'
dh = '15'
dm = '00'
matrix = [[None]*(len(routeList)) for n in range(len(routeList))]
info = []
progCount=1

###set up robobrowser
alert("setting up browser")
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

###fill out form
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

###get the fare and journey breakdown
def journeyDts(html):
    global info
    farebd = html.find_all(class_="fare-breakdown")
    spanID = 'type="hidden" value=(.+?)/>'
    regex = (spanID)
    pattern = re.compile(regex)
    price = pattern.findall(str(farebd))
    info = []
    for line in price:
        pattern = re.findall(r'\d+', line)
        info.append([float(''.join([pattern[1],'.',pattern[2]])),None])

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
#     

###progress counter
def progress(rlength):
    global progCount
    n = rlength - 1
    incr = int(100/(n*(n+1)/2))
    print(progCount*incr,'% complete...')
    progCount+=1
    
###matrix coordinates
def fillMatrix():
    length = len(routeList)   
    x = 0
    y = 1
    lb()
    alert('gathering route data')
    while x!=length and y!=length:
        progress(len(routeList))
        formFill(routeList[x],routeList[y],dd,dh,dm)
        matrix[x][y]=info[0][0]
        y+=1
        if y==length:
            x+=1
            y=x+1        
    print('100 % complete...')

lb()
print(matrix)

