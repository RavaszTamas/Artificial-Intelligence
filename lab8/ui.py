# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 13:36:55 2020

@author: tamas
"""


import matplotlib as mpl


class Console():
    
    
    def __init__(self,controller):
        self.__controller = controller
    def __printMenu(self):
        s = ""
        #s +="Default ratio between training data and test data is 0.3 ( from a 100 70 is for training 30 is for test)\n"
        s += "I split of the input data into 80% training data and 20% test data in a random method. The final test loss is based on that\n"
        s += "A small learning rate is suggested because even with normalization it can cause overflow errors because of the randomness\n"
        s += "1. Train network  which uses matrices, my homework solution.\n"
        #s += "2. Train network with \"long\" ANN, just to see how it works .\n"
        s += "0. Exit.\n"
        print(s)
        
    def __readInput(self):
        iterations = 1000
        try:
            print("Input the size of the number of iterations  1000 is the implicit value")
            iterations = int(input("iterations = "))
            if iterations <= 0:
                raise Exception
        except :
            print("invalid number, the implicit value is still 1000")
            iterations=1000
        learningrate = 0.01
        try:
            print("Input the size of the learning rate implicit value is 0.01")
            print("This value is suggested because of overflow errors")
            learningrate = float(input("rate = "))
            if learningrate <= 0:
                raise Exception
        except :
            print("invalid number, the implicit value is still 0.01")
            learningrate=0.01
        hiddenLayerNeuronCount = 5
        try:
            print("Input the number of neurons in the hidden layer rate implicit value is 5")
            hiddenLayerNeuronCount = int(input("count = "))
            if hiddenLayerNeuronCount <= 0:
                raise Exception
        except :
            print("invalid number, the implicit value is still 5")
            hiddenLayerNeuronCount=5

        return iterations,learningrate,hiddenLayerNeuronCount
        
    '''
    def __trainNetworkLong(self):
        print("this one will be slow")
        iterations,learninRate,hiddenLayerSize = self.__readInput()
        result = self.__controller.trainNetworkLongAnn(iterations,learninRate,hiddenLayerSize)
        print('long version finished')
        
        mpl.pyplot.plot(result[0], result[1], label='loss value vs iteration')
        mpl.pyplot.xlabel('Iterations')
        mpl.pyplot.ylabel('loss function')
        mpl.pyplot.legend()
        mpl.pyplot.show()
    '''

        
    def __trainNetworkMatrix(self):
        iterations,learninRate,hiddenLayerSize = self.__readInput()
        result = self.__controller.trainNetworkMatrix(iterations,learninRate,hiddenLayerSize)
        print(result[2])
        print()
        print("Before this the final output can be seen")
        print()
        print("initial loss:" + str(result[3]) + " final loss: " + str(result[4]) + " test loss " + str(result[5]))
        print("matrices finished")
        mpl.pyplot.plot(result[0], result[1], label='loss value vs iteration')
        mpl.pyplot.xlabel('Iterations')
        mpl.pyplot.ylabel('loss function')
        mpl.pyplot.legend()
        mpl.pyplot.show()
        

    def run(self):
        while True:
            self.__printMenu()
            inputCommand = input().strip()
            if inputCommand== "1":
                self.__trainNetworkMatrix()
            elif inputCommand== "0":
                return
