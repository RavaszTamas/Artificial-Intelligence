# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 13:49:13 2020

@author: tamas
"""

from Controller import Controller

class Console():
    
    
    def __init__(self):
        self.__controller = Controller(3,100,0.3,10000)
        
    
    def __executeEvolutionaryAlgorithm(self):
        
        return self.__controller.startEvolutionary()
    
    def __printMenu(self):
        s =""
        s +="0. Exit\n"
        s +="1. Read new configuration\n"
        s +="2. Evolutionary Algorithm\n"
        s +="3. Hill climbing\n"
        print(s)
    def __readNewConfiguration(self):
        problemSize = 3
        try:
            print("Input the number of rows of the matrix (implicit 3)")
            problemSize = int(input("problemSize = "))
            if problemSize <= 0:
                raise Exception
        except :
            print("invalid number, the implicit value is still 3")
            problemSize=3
            
        populationSize = 100
        try:
            print("Input the population size (implicit 100)")
            populationSize = int(input("populationSize = "))
            if populationSize <= 0:
                raise Exception
        except :
            print("invalid number, the implicit value is still 100")
            populationSize=100
            
        probabilityMutation = 0.3
        try:
            print("Input the probabilty for mutation and crossover (implicit 0.3)")
            probabilityMutation = float(input("probabilityMutation = "))
            if probabilityMutation <= 0.0:
                raise Exception
            if probabilityMutation >= 1.0:
                raise Exception
        except :
            print("invalid number, the implicit value is still 0.3")
            probabilityMutation=0.3
        numberOfIterations = 10000
        try:
            print("Input the number of iterations (implicit 10000)")
            numberOfIterations = int(input("numberOfIterations = "))
            if numberOfIterations <= 0:
                numberOfIterations = 10000
        except :
            print("invalid number, the implicit value is still 10000")
            numberOfIterations=10000


        self.__controller = Controller(problemSize,populationSize,probabilityMutation,numberOfIterations)

    def __executeHillClimbing(self):
        return self.__controller.startHillClimbing()
    
    def __printHillClimbingResult(self,result):

        print("Final fitness (0 is the best value) = " + str(result[0]) + " after " + str(result[2]) + " iterations.")
        matrixToCheck = result[1]
        #print(matrixToCheck)
        for i in range(len(matrixToCheck)//2):
            for j in range(len(matrixToCheck)//2):
                print("("+str(matrixToCheck[i][j]) +","+str(matrixToCheck[i+len(matrixToCheck)//2][j])+") ",end="")
            print()

    def __printResultEvolutionary(self,result):

        print("Final fitness (0 is the best value) = " + str(result[0]) + " after " + str(result[2]) + " iterations.")
        matrixToCheck = result[1]
        #print(matrixToCheck)
        for i in range(len(matrixToCheck)//2):
            for j in range(len(matrixToCheck)//2):
                print("("+str(matrixToCheck[i][j]) +","+str(matrixToCheck[i+len(matrixToCheck)//2][j])+") ",end="")
            print()
    def run(self):
        while True:
            self.__printMenu()
            choice = input()
        
            if choice == "0":
                return            
            elif choice == "1":
                self.__readNewConfiguration()
            elif choice == "2":
                result = self.__executeEvolutionaryAlgorithm()
                self.__printResultEvolutionary(result)
            elif choice == "3":
                result = self.__executeHillClimbing()
                self.__printHillClimbingResult(result)