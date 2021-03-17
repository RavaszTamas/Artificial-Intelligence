# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 15:17:52 2020

@author: tamas
"""

class View():
    
    def __init__(self,geneticTreeModel,filename="output.out"):
        self.__geneticTreeModel = geneticTreeModel
        self.__filename = filename
    
    def printMessage(self,message):
        print(message)
        
    def printMenu(self):
        s = "\n"
        s += "begin - begin the evaluation\n"
        s += "exit - exit the application\n"
        s += "\n"
        print(s)
        
    def printResult(self):
        
        pop,stats,hof,testResult = self.__geneticTreeModel.obtainLastResult()
        
        record = stats.compile(pop)

        s = ""
        s += "The minimum fitness was: " + str(record['min']) + "\n"
        s += "The average fitness was: " + str(record['avg']) + "\n"
        s += "The maximum fitness was: " + str(record['max']) + "\n"
        s += "The standard deviation fitness was: " + str(record['std']) + "\n"
        print(s)
        s = ""
        s += "The obtained best function/tree is:"
        print(s)
        print(hof[0])
        print("The test result was: " + str( testResult * 100) + "%")