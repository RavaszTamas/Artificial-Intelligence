# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 20:19:24 2020

@author: tamas
"""

import random, copy
from domain import NeuralNetwork, linear_function,derivative_linear
from sklearn.model_selection import train_test_split
from repository import Repository
import numpy as np
import matplotlib.pyplot as plt
import math
from sklearn import linear_model
import matplotlib as mpl

class Controller():
    
    
    def __init__(self,repository):
        self.__repository = repository
        self.__network = None
    
    def __normalizeInput(self,initialData):
        
        newInput = np.empty((0,initialData.shape[1]),int)
        xMin = np.amin(initialData)
        xMax = np.amax(initialData)
        #print((xMin,xMax))
        #print(newInput.shape)
        for X in initialData:
            xNew = (X - xMin)/(xMax-xMin)
            #print(xNew)
            #print(xNew)
            newInput = np.append(newInput,[xNew],axis=0)
        return newInput
    
    
    def trainNetworkMatrix(self,numberOfIterations,learningRate,hiddenLayerSize):
        initialData = np.asarray(self.__repository.getAllData())
        initialData = self.__normalizeInput(initialData)
        X = initialData[:,:len(initialData[0])-1]
        Y = initialData[:,len(initialData[0])-1]

        X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2)
        y_train = y_train.reshape(-1,1)
        y_test = y_test.reshape(-1,1)
        

        
        self.__network = NeuralNetwork(X_train, y_train, hiddenLayerSize , linear_function,derivative_linear)

        iterations =[]
        for i in range(numberOfIterations):
            self.__network.feedForward()
            self.__network.backprop(learningRate)
            iterations.append(i)
        
        initialLoss = self.__network.loss[0]
        finalLoss = self.__network.loss[-1]
        
        self.__network.setInput(X_test)
        self.__network.feedForward()
        testLoss = sum((y_test - self.__network.getOutput())**2)

        return (iterations,self.__network.getLoss(),self.__network.getOutput(),initialLoss,finalLoss,testLoss)
        
    '''
    def trainNetworkLongAnn(self,numberOfIterations,learningRate,hiddenLayerSize):
        initialData = np.asarray(self.__repository.getAllData())
    
        initialData = self.__normalizeInput(initialData)
        
    
        X = initialData[:,:len(initialData[0])-1]
        Y = initialData[:,len(initialData[0])-1]
    
        X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2)
        y_train = y_train.reshape(-1,1)
        y_test = y_test.reshape(-1,1)
        
        
        
        self.__network = Network([5,hiddenLayerSize,1],linear_function,derivative_linear)
        
        errors =[]
        iterations =[]
        for i in range(numberOfIterations):
            iterations.append(i)
            e = []
            for j in range(len(X_train)):
                e.append(self.__network.computeLoss(X_train[j],y_train[j])[0])
                self.__network.backPropag(self.__network.computeLoss(X_train[j],y_train[j]), learningRate)
            errors.append(sum([x**2 for x in e]))
        for j in range(len(X_train)):
            print(X_train[j], y_train[j], self.__network.feedForward(X_train[j]))
        print(str(self.__network))
        
        return iterations,errors
    '''
        
        
        
        