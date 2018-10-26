import sys
import numpy as np

leftMatrix = []
rightMatrix = []
lineArr = []
usedAlfa = []

def usedAlfaFun(file):
    file = open(sys.argv[1], "r")
    lineCounter = 0
    for line in file:
       lineArr.append(line)
       for letter in line:
           if letter.isalpha()== True:
               if letter not in usedAlfa: usedAlfa.append(letter)
       lineCounter = lineCounter + 1

    return usedAlfa


usedAlfa = usedAlfaFun(file)
file = open(sys.argv[1], "r")
for line in file:
   coefficientArr = []
   for letter in usedAlfa:
       coefficientArr.append(0)
   lineSplit = (line.split("="))
   lineSplit[1] = lineSplit[1].strip("\n")
   constant = int(lineSplit[1].strip(" "))
   for index, letter in enumerate(lineSplit[0]):
        if (letter.isalpha() == True):
            coefficient = lineSplit[0][index-1]
            if letter != lineSplit[0][index]: coefficientArr.append(0)
            if coefficient == " " or coefficient == "": coefficient = 1
            if coefficient == "-": coefficient = -1
            else: coefficient = int(coefficient)
            if lineSplit[0][index-2] == "-": coefficient = coefficient * -1
            for index2, alfa in enumerate(usedAlfa):
                if alfa == lineSplit[0][index]: coefficientArr[index2] = (coefficient)
   leftMatrix.append(coefficientArr)
   rightMatrix.append(constant)

leftMatrixN = np.array(leftMatrix)
rightMatrixN = np.array(rightMatrix)
matrixRank = np.linalg.matrix_rank(leftMatrixN)
rightMatrixN = (np.expand_dims(rightMatrixN, axis=1))
extendedMatrix = (np.hstack((leftMatrixN, rightMatrixN)))


try:
    results = np.linalg.solve(leftMatrix, rightMatrix)
    resultStr = "solution: "
    for index, item in enumerate(results):
        resultStr = resultStr + (usedAlfa[index] + "=" + str(item) + ", ")
    resultStr = resultStr.strip(", ")
    print(resultStr)
except:
    if len(usedAlfa) != len(leftMatrixN):
            spaceDim = len(usedAlfa) - len(leftMatrixN)
            print("solution space dimension: " + str(spaceDim))

    if np.linalg.matrix_rank(extendedMatrix) != matrixRank:
        print("no solution")
