# -*- coding: utf-8 -*-
"""
Created on Fri May 15 11:40:00 2020

@author: tamas
"""

class Console():
    
    def __init__(self,controller):
        self.__controller = controller
        
    def __printMenu(self):
        s = ""
        s += "1. Train CNN.\n"
        s += "0. Exit.\n"
        print(s)
        
    def __readInput(self):
        print()
        epochs = 10
        try:
            print("Input the size of the number of epochs  10 is the implicit value")
            epochs = int(input("epochs = "))
            if epochs <= 0:
                raise Exception
        except :
            print("invalid number, the implicit value is still 10")
            epochs=10
            
        print()
        
        inputDataSize = 10
        try:
            print("Input the size of input, number of used pictures to train the network  1000 is the implicit value")
            print("Minimum 1000, maximum 60000")
            inputDataSize = int(input("inputDataSize = "))
            if inputDataSize < 1000:
                raise Exception
            if inputDataSize > 60000:
                raise Exception

        except :
            print("invalid number, the implicit value is still 1000")
            inputDataSize=1000

        return epochs,inputDataSize
        
    def __trainCNN(self):
        epochs,inputDataSize = 10,1000
        epochs,inputDataSize = self.__readInput()
        result = self.__controller.trainCNNKeras(epochs,inputDataSize)
        print("Loss: " + str(result[0]))
        print("Accuracy: " + str(result[1]))

    def run(self):
        
        while True:
            self.__printMenu()
            inputCommand = input().strip()
            if inputCommand== "1":
                self.__trainCNN()
            elif inputCommand== "0":
                return
            
            
    