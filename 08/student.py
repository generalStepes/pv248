import pandas as pd
from statistics import mean, median
import sys
import json
from scipy import stats, optimize
from datetime import datetime, timedelta

file = pd.read_csv(sys.argv[1])
columns = list(file.head(0))

def aggregateStuff(file):
    aggPoints = []
    numberOfStudent = (len(file[columns[0]]))
    for column in columns[1:]:
        aggPoints.append(sum(file[column])/numberOfStudent)
    aggPoints = pd.Series(aggPoints)
    aggPoints.index = columns[1:]
    #print(aggPoints)
    return(aggPoints)


def daysTillBang(slope):
    sixteenPoints = 16/slope
    twentyPoints = 20/slope
    semBeg = datetime.strptime("2018-09-17", "%Y-%m-%d")
    sixteenPoints = semBeg + timedelta(days=sixteenPoints)
    sixteenPoints = sixteenPoints.strftime("%Y-%m-%d")
    twentyPoints = semBeg + timedelta(days=twentyPoints)
    twentyPoints = twentyPoints.strftime("%Y-%m-%d")
    return sixteenPoints, twentyPoints

def getDates(columns):
    semBeg = datetime.strptime("2018-09-17", "%Y-%m-%d")
    datesSinceBeg = []
    uniqueDates = []
    for date in columns[0:]:
        slash = date.find("/")
        date = date[:slash]
        date = date.strip(" ")
        dateObject = datetime.strptime(date, "%Y-%m-%d")
        dateDiff = (dateObject - semBeg)
        dateDiff = int(dateDiff.days)
        if dateDiff not in datesSinceBeg:
            uniqueDates.append(date)
            datesSinceBeg.append(dateDiff)
    return(datesSinceBeg, uniqueDates)

def getCumPoints(selStudent, columns, uniqueDates):
    dateArr = []
    cumulTemp = 0
    for date in uniqueDates:
        for column in columns:
            if (column.find(date)) != -1:
                cumulTemp += selStudent[column]
        dateArr.append(cumulTemp)
    return dateArr

if sys.argv[2] != "average":
    selectedStudentPre = file[file["student"]==int(sys.argv[2])]
    selectedStudent = []
    for column in columns[1:]:
        selectedStudent.append(selectedStudentPre[column].values[0])
    selectedStudent = pd.Series(selectedStudent)
    selectedStudent.index = columns[1:]
else:
    selectedStudent = aggregateStuff(file)
selectedStudent = selectedStudent.sort_index()
columns = (list(selectedStudent.index))
indexes = selectedStudent.index
execDict = {}

for i, row in enumerate(selectedStudent):
    currIndex = indexes[i]
    slash = currIndex.find("/")
    currIndex = currIndex[slash+1:]
    if currIndex not in execDict:
        execDict[currIndex] = row
        #execDict[currIndex].append(row)
    else:
        execDict[currIndex] += row

execDict = pd.Series(execDict)

dateArr= {}
dateArr["mean"] = round(mean(execDict), 15)
dateArr["median"] = round(median(execDict),15)
dateArr["total"] = round(sum(execDict),15)

counter = 0
for note in execDict:
    if note > 0: counter += 1
dateArr["passed"] = counter

datesSinceBeg, uniqueDates = getDates(columns)
cumPoints = getCumPoints(selectedStudent, columns, uniqueDates)
#slope, intercept, r_value, p_value, std_err = stats.linregress(cumPoints, datesSinceBeg)
slope = optimize.curve_fit(lambda x, m: m*x, datesSinceBeg, cumPoints)[0][0]
dateArr["regression slope"] = round(slope, 15)

if slope != 0:
    sixteenPoints, twentyPoints = daysTillBang(slope)
    dateArr["date 16"] = sixteenPoints
    dateArr["date 20"] = twentyPoints
else:
    dateArr["date 16"] = "inf"
    dateArr["date 20"] = "inf"


print(json.dumps(dateArr, ensure_ascii=False, indent=2))