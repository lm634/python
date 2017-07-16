# set up matrix


################################################################################

matrix=[[None, 4.4, 11.3, 16.2, 21.3, 14.5, 14.5, 36.4, 40.0, 119.0],
[None, None, 7.2, 12.0, 14.5, 14.5, 14.5, 14.5, 1.38, 43.8],
[None, None, None, 7.3, 12.2, 19.6, 19.6, 1.21, 1.38, 42.2],
[None, None, None, None, 8.0, 12.2, 17.1, 10.3, 9.9, 17.9],
[None, None, None, None, None, 10.1, 11.2, 13.4, 9.7, 15.3],
[None, None, None, None, None, None, 7.3, 12.2, 9.2, 9.7],
[None, None, None, None, None, None, None, 8.5, 9.2, 9.7],
[None, None, None, None, None, None, None, None, 13.2, 17.3],
[None, None, None, None, None, None, None, None, None, 10.5],
[None, None, None, None, None, None, None, None, None, None]]

global matrix
totals = []
runningTotal = 0
x = []
temp = 0
for item in range(len(matrix[0])):
    x.append(temp)
    temp+=1 
y = [0]
low = 9999999

def lb():
    print()
    
def sum(list):
    global runningTotal
    runningTotal = 0
    for item in list:
        runningTotal = runningTotal+item
################################################################################

###### STEP ONE
for item in matrix[0]:
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

###### STEP 2
while len(y) < len(x):
    for i in range(len(x)):
        yLen = len(y)-1
        if i not in y and matrix[yLen][i] != None and matrix[yLen][i] < 9999999:
            loL = 1
            global hist
            hist = []
            hist.append(matrix[yLen][i])
            newX = totals[yLen][1]
            newY = yLen
            while True:
                prevStep = matrix[newX][newY]
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

print('totals = ',totals)
print('\ny = ',y,'\n')
        
        

