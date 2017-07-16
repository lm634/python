### Scraping Stock Data from Yahoo Finance ###

#--->setup<---#

#libraries
#pip3 install urllib3
print ('>>> initialising...')
import urllib.request as ur
from datetime import datetime
import os
import csv
import urllib3
import time
import re
import itertools
print ('>>> libraries imported...')

#setting the directory
save_path = '/Users/.../stockTexts/'
current_path = os.getcwd()
new_path = os.chdir(save_path)
print ('>>> directory established...')

#creating lists
dir_index = []
i = datetime.now()
thyme = i.strftime('%Y%m%d%H%M%S')
date = i.strftime('Y%m%d')
acronym_index = []
acronymIndex = []
lcAcronymIndex = []
indexInterval = []
urlIndex = []

#creating library and files
with open('inits/stockRefs.csv') as id:
    csv_id = csv.reader(id)
    for row in csv_id:
        acronym_index.append(row[0])
        temp_path = ' - '.join(row)
        dir_index.append(temp_path)
        file_path = '/Users/.../stockTexts/library/'+temp_path+'/'
        if not os.path.exists(file_path):
            os.makedirs(file_path)
            new_path = os.chdir(file_path)
#IF FILE DOESN'T EXIST CREATE THE FILE           
            new_csv = open ((row[0])+date+'.csv', 'w')
            new_csv.write('file ')
            new_csv.write(time+' ')
            new_csv.write(temp_path+'\n')
            new_csv.write ('date and time\n')
            new_csv.write ('price\n')
            new_csv.write ('previous close\n')
            new_csv.write ('open price\n')
            new_csv.write ('1 year target estimate\n')
            new_csv.write ('beta\n')
            new_csv.write ('next earnings date\n')
            new_csv.write ('average volume (3 month)\n')
            new_csv.write ('pe (ttm)\n')
            new_csv.write ('annual eps estimate\n')
            new_csv.write ('mean recommendation\n')
            new_csv.write ('peg ratio (5 year)\n')
            new_csv.write ('bid volume\n')
            new_csv.write ('ask price\n')
            new_csv.write ('ask volume\n')
            new_csv.write ('volume\n')
            new_csv.write ('time elapsed')
            new_csv.close()
    print ('>>> folder structure built...')
print ('>>> files verified...')
id.close()
new_path = os.chdir(save_path)

#lists and datetime
print ('>>> initialisation complete')

#--->define functions and verify data<---#
#commence loop to get data from yahoofinance
with open ('inits/stockRefs.csv') as f:
    stockIndex = csv.reader(f)
    for row in stockIndex:
        acronymIndex.append(row[0])
for row in acronymIndex:
    url_ref = ('https://uk.finance.yahoo.com/q?s='+row+'.L')
    urlIndex.append(url_ref)
    lowercase = (row.lower())+'.l'
    lcAcronymIndex.append(lowercase)

#data check
i_len = (len(acronymIndex))
u_len = (len(urlIndex))
errorI = '>>> not enough data <<<'
err_len = i_len - u_len
if err_len >= 1:
    print ('>>> error: mismatch in data length <<<')
    print ('>>> terminating programme <<<')
    quit()
else:
    refDict = zip(urlIndex, lcAcronymIndex)
    print ('>>> loading functions, please wait...')

#functions - market data
def webIndex():
    spanID = '<div class="title"><h2>(.+?)</h2>'
    regex = (spanID)
    pattern = re.compile(regex)
    web_index = pattern.findall(str(htmltext))
    web_index = ''.join(web_index)
    banner = str('\n>>> '+web_index+' // '+(row[1])+' ...\n')
    dataWrite.append(banner)
    print (banner)
    print (row[0])

def overallPrice():
    spanID = '<span id="yfs_l84_'+(row[1])+'">(.+?)</span>'
    regex = (spanID)
    pattern = re.compile(regex)
    price = pattern.findall(str(htmltext))
    if len(price) < 1:
        while len(price) < 1:
            price.append(errorI)
    price = ''.join(price)
    price = price.replace(',', '')
    dataWrite.append(price)

def tableValues():
    spanID = '<td class="yfnc_tabledata1">(.+?)</td>'
    regex = (spanID)
    pattern = re.compile(regex)
    tableValues = pattern.findall(str(htmltext))
    if len(tableValues) < 25:
        while len(tableValues) < 25:
            tableValues.append(errorI)
    prevClose = tableValues[0]
    prevClose = prevClose.replace(',', '')
    dataWrite.append(prevClose)
    openPrice = tableValues[1]
    openPrice = openPrice.replace(',', '')
    dataWrite.append(openPrice)
    yrTargetEst = tableValues[4]
    yrTargetEst = yrTargetEst.replace(',', '')
    dataWrite.append(yrTargetEst)
    beta = tableValues[5]
    beta = beta.replace(',', '')
    dataWrite.append(beta)
    nextEarningsDate = tableValues[6]
    nextEarningsDate = nextEarningsDate.replace(',', '')
    dataWrite.append(nextEarningsDate)
    avgVol3M = tableValues[10]
    avgVol3M = avgVol3M.replace(',', '')
    dataWrite.append(avgVol3M)
    p_e_ttm = tableValues[12]
    p_e_ttm = p_e_ttm.replace(',', '')
    dataWrite.append(p_e_ttm)
    eps_ttm = tableValues[13]
    eps_ttm = eps_ttm.replace(',', '')
    dataWrite.append(eps_ttm)
    forward_p_e = tableValues[15]
    forward_p_e = forward_p_e.replace(',', '')
    dataWrite.append(forward_p_e)
    p_s_ttm = tableValues[16]
    p_s_ttm = p_s_ttm.replace(',', '')
    dataWrite.append(p_s_ttm)
    annual_epsEst = tableValues[18]
    annual_epsEst = annual_epsEst.replace(',', '')
    dataWrite.append(annual_epsEst)
    meanRec_b1s5 = tableValues[20]
    meanRec_b1s5 = meanRec_b1s5.replace(',', '')
    dataWrite.append(meanRec_b1s5)
    peg_ratio_5yr = tableValues[21] 
    peg_ratio_5yr = peg_ratio_5yr.replace(',', '')
    dataWrite.append(peg_ratio_5yr)

def bidPrice():
    spanID = '<span id="yfs_b00_'+(row[1])+'">(.+?)</span>'
    regex = (spanID)
    pattern = re.compile(regex)
    bid_price = pattern.findall(str(htmltext))
    if len(bid_price) < 1:
        while len(bid_price) < 1:
            bid_price.append(errorI)
    bid_price = ''.join(bid_price)
    bid_price = bid_price.replace(',', '')
    dataWrite.append(bid_price)

def bidVol():
    spanID = '<span id="yfs_b60_'+(row[1])+'">(.+?)</span>'
    regex = (spanID)
    pattern = re.compile(regex)
    bid_vol = pattern.findall(str(htmltext))
    if len(bid_vol) < 1:
        while len(bid_vol) < 1:
            bid_vol.append(errorI)
    bid_vol = ''.join(bid_vol)
    bid_vol = bid_vol.replace(',', '')
    dataWrite.append(bid_vol)

def askPrice():
    spanID = '<span id="yfs_a00_'+(row[1])+'">(.+?)</span>'
    regex = (spanID)
    pattern = re.compile(regex)
    ask_price = pattern.findall(str(htmltext))
    if len(ask_price) < 1:
        while len(ask_price) < 1:
            ask_price.append(errorI)
    ask_price = ''.join(ask_price)
    ask_price = ask_price.replace(',', '')
    dataWrite.append(ask_price)

def askVol():
    spanID = '<span id="yfs_a50_'+(row[1])+'">(.+?)</span>'
    regex = (spanID)
    pattern = re.compile(regex)
    ask_vol = pattern.findall(str(htmltext))
    if len(ask_vol) < 1:
        while len(ask_vol) < 1:
            ask_vol.append(errorI)
    ask_vol = ''.join(ask_vol)
    ask_vol = ask_vol.replace(',', '')
    dataWrite.append(ask_vol)

def volume():
    spanID = '<span id="yfs_v53_'+(row[1])+'">(.+?)</span>'
    regex = (spanID)
    pattern = re.compile(regex)
    volume = pattern.findall(str(htmltext))
    if len(volume) < 1:
        while len(volume) < 1:
            volume.append(errorI)
    volume = ''.join(volume)
    volume = volume.replace(',', '')
    dataWrite.append(volume)

#--------------------------------------------------------------------->>>
### FINAL VERSION NEEDS TO WRITE TO THE CORRECT DIRECTORY, ALSO NOT 
### OVERWRITE EXISTING DATA, APPEND TO THE END OF CSV  
def tempWritingFunc():
    txtfl = (row[1]+'.'+date+'.csv')
    #if txtfile exists in location already:
    file_path = '/Users/.../stockTexts/library/'+txtfl+'/'
    if not os.path.exists(file_path):
        os.makedirs(file_path)
        csvfl = open (txtfl+'', 'w')
        for item in dataWrite:
            csvfl.write (item)
            csvfl.write ('\n')
            csvfl.close()
    else:
#        txtfl = open ((row[1]+'.'+time+'.csv'), 'w')
#        for item in dataWrite:
#            txtfl.write (item)
#            txtfl.write ('\n')
#            txtfl.close()
        print ('>>> stock data stored...')
#--------------------------------------------------------------------->>>

def timerEnd():
    v = datetime.now()
    intIndex = str(v - iv)
    indexInterval.append(intIndex)
# NEED TO FIX DECIMAL PLACE BUG!!!
    print ('>>> time elapsed = '+intIndex)
    dataWrite.append(intIndex)

def overallCounter():
    iii = datetime.now()
    timeiii = iii.strftime('%H:%M:%S.%f')
    totElapsed = str(iii - ii)
    print ('>>> total time elapsed... '+totElapsed)

def counterSave():
    csvfl = open(('temps/timers/timeranalysis'+thyme+'.csv'), 'w')
    for item in indexInterval:
        csvfl.write (item)
        csvfl.write('\n')
    csvfl.close()

#functions loaded    
print ('>>> functions loaded...')
print ('>>> accessing stock data, please wait...')

#--->define running times and start loop<---#
#run only 9-5
i=datetime.now()
if (int(i.strftime('%H'))) < 9 or (int(i.strftime('%H'))) > 17:
    print ('>>> awaiting next stock market open time, please wait...')
    while True:
        i=datetime.now()
        time.sleep(10)
        if (int(i.strftime('%H'))) == 9:
            break

#start timers, find the url and gather data
ii=datetime.now()
while True:
    i=datetime.now()
    for row in refDict:
        iv = datetime.now()
        dataWrite = []             
        with ur.urlopen(row[0]) as response:
            htmltext = response.read()
            webIndex()
            overallPrice()
            tableValues()
            bidPrice()
            bidVol()
            askPrice()
            askVol()
            volume()
            tempWritingFunc()
            timerEnd()
    if (int(i.strftime("%H"))) < 16:
        break

#--->save timer data and close<---#
#save all timer information
print ('\n>>> all data compiled, exiting programme...')
overallCounter()
counterSave()

#--->save all files online<---#

#end programme
print ('>>> all data saved, goodbye...')
quit()    
