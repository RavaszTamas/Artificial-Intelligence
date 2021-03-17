# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 20:19:24 2020

@author: tamas
"""

import random, copy
from domain import InvalidInputDataException
import numpy as np
import matplotlib.pyplot as plt
import math
from sklearn import linear_model

class Controller():
    
    
    def __init__(self,repository):
        self.__repository = repository


    def solveLeastSquares(self,treshold):
        initialData = np.asarray(self.__repository.getAllData())
        X = initialData[:,:len(initialData[0])-1]
        Y = initialData[:,len(initialData[0])-1]
        
        X = np.insert(X,0,1,axis=1)
        
        X_T = X.transpose()
        Y = Y.reshape(-1,1)
        
        coefficients = X_T.dot(X)
        
        coefficients = np.linalg.inv(coefficients)
        
        coefficients = coefficients.dot(X_T)
        
        coefficients = coefficients.dot(Y)
        
        '''
        X = np.matrix(X)
        X_T = np.matrix(X.transpose())
        Y = np.matrix(Y.reshape(-1,1))1
        coefficients = (X_T*X).I*X_T*Y
        '''
        testResult = self.__testCoefficients(coefficients.flatten(),initialData,treshold)
        
        return coefficients.flatten(),testResult
    
    def __testCoefficients(self,coefficients,initialData,treshold):
        X = initialData[:,:len(initialData[0])-1]
        Y = initialData[:,len(initialData[0])-1]
        
        errors = []
        
        for i in range(len(X)):
            val = coefficients[0]
            for j in range(len(X[i])):
                val += coefficients[j+1] * X[i][j]
            '''
            Checking the result is larger than the pre defined treshold
            '''
            if abs(Y[i]-val) >= treshold:
                print(val,math.floor(val))
                errors.append((abs(Y[i]-val),i,j))
        return errors