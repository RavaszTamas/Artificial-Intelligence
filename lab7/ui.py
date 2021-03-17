# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 13:36:55 2020

@author: tamas
"""


from domain import InvalidInputDataException


class Console():
    
    
    def __init__(self,controller):
        self.__controller = controller
    def __printMenu(self):
        s = ""
        #s +="Default ratio between training data and test data is 0.3 ( from a 100 70 is for training 30 is for test)\n"
        s += "1. Solve regression with least squares method.\n"
        s += "0. Exit.\n"
        print(s)
        
    def __readTreshold(self):
        treshold = 0.4
        try:
            print("Input the size of the treshold for result validation 0.4 is the implicit value, 0 is also available")
            treshold = float(input("treshold = "))
            if treshold < 0:
                raise Exception
        except :
            print("invalid number, the implicit value is still 0.4")
            treshold=0.4
        return treshold

    def __solveLeastSquares(self):
        
        treshold = self.__readTreshold()
        
        resultCoefficients,errors = self.__controller.solveLeastSquares(treshold)
        stringToPrint = "f(X1"
        for i in range(2,len(resultCoefficients)):
            stringToPrint += ",X" + str(i)
            
        stringToPrint += ") = " +str(resultCoefficients[0])
    
        for i in range(1,len(resultCoefficients)):
            stringToPrint += " + " +str(resultCoefficients[i]) + " * X" + str(i)
        
        print("Errors larger than "+str(treshold)+":")
        for elem in errors:
            print("value: " +str(elem[0]) + ", row:" + str(elem[1]) + ", column:"  + str(elem[2]))
        if len(errors) == 0:
            print("No errors larger than " +str(treshold)+"!")
            
        print()
        print("Resulting function:")
        print(stringToPrint)
        
        
    def run(self):
        while True:
            try:
                self.__printMenu()
                inputCommand = input().strip()
                if inputCommand== "1":
                    self.__solveLeastSquares()
                elif inputCommand== "0":
                    return
            except InvalidInputDataException as ex:
                print(str(ex) + "\nTry a different ratio")