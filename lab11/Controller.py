# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 15:15:47 2020

@author: tamas
"""

import View
import csv
import Classification
import numpy as np
class Controller:
    
    def __init__(self, filename="input.in"):
        self.__inputs = []
        self.__filename = filename
        self.__inputTerminals = None
        self.__initialData = None
        self.__readInputs()
        self.__system = Classification.GeneticTreeModel(self.__initialData, self.__inputTerminals)
        self.__view = View.View(self.__system)

    
    def __readInputs(self):
        self.__inputTerminals = []
        with open(self.__filename, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                self.__inputTerminals += row
        
        self.__inputTerminals = [float(i) for i in self.__inputTerminals]
        
        self.__initialData = []
        with open('sensor_readings_24.data', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                self.__initialData.append(row)
        self.__initialData = np.array(self.__initialData)
    def __readUserInput(self):
        iterations = 40
        try:
            iterations = int(input("Please enter the number of iterations: "))
            if iterations <= 0:
                raise Exception
        except Exception:
            print("Invalid input iterations is still 40")
            iterations = 40
            
            
        populationNumber = 100
        try:
            populationNumber = int(input("Please enter the population size: "))
            if populationNumber <= 0:
                raise Exception
        except Exception:
            print("Invalid input the population size is still 100")
            iterations = 100

            
            
        return iterations,populationNumber
    def __evalute(self):
        iterations,populationNumber = self.__readUserInput()
        self.__system.evaluate(iterations,populationNumber)
        self.__view.printResult()
        
    def start(self):
        
        while True:
            self.__view.printMenu()
            command = input("enter the command: ")
            if command == "begin":
                self.__evalute()
            elif command == "exit":
                return
            else:
                print("Invalid input")
                
                
