import sys
import numpy as np

leftMatrix = []

file = open(sys.argv[1], "r")
for line in file:
   coefficientArr = []
   lineSplit = (line.split("="))
   lineSplit[1] = lineSplit[1].strip("\n")
   constant = lineSplit[1].strip(" ")
   for index, letter in enumerate(lineSplit[0]):
        if (letter.isalpha() == True):
            coefficient = lineSplit[0][index-1]
            if coefficient == " " or coefficient == "": coefficient = 1
            if coefficient == "-": coefficient = -1
            else: coefficient = int(coefficient)
            if lineSplit[0][index-2] == "-": coefficient = coefficient * -1
            coefficientArr.append(coefficient)
   leftMatrix.append(coefficientArr)
   print(np.array(leftMatrix))
