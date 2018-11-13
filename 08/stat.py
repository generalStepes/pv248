import pandas as pd
from statistics import mean, median

file = pd.read_csv("points.csv")
columns = list(file.head(0))


dateArr = {}
for i in range(1,len(columns)):
    colName = columns[i].strip(" ")
    slahPos = colName.find("/")
    colName = colName[:slahPos]
    dateArr[colName] = {}
    dateArr[colName]["mean"] = round(mean(file[columns[i]]),1)
    dateArr[colName]["median"] = median(file[columns[i]])
    dateArr[colName]["first"] = file[columns[i]].quantile(.25)
    dateArr[colName]["last"] = file[columns[i]].quantile(0.75)

print(dateArr)
