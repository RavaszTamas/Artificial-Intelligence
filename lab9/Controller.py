# -*- coding: utf-8 -*-
"""
Created on Fri May 15 11:39:56 2020

@author: tamas
"""

from Repository import Repository
import tensorflow as tf
from Domain import CNNKeras
import matplotlib.pyplot as plt
import numpy as np
class Controller():
    def __init__(self,repository):
        self.__repository = repository
        
        
    def __prepareKerasData(self,trainX,trainY,testX,testY):
        trainX = trainX.reshape(trainX.shape[0], 28, 28, 1)
        testX = testX.reshape(testX.shape[0], 28, 28, 1)
        input_shape = (28, 28, 1)
        trainX = trainX.astype('float32')
        testX = testX.astype('float32')
        trainX /= 255
        testX /= 255
        return trainX,trainY,testX,testY,input_shape
    
    def trainCNNKeras(self,epochs,inputDataSize):
        trainX,trainY,testX,testY = self.__repository.getTrainingDataKeras()
        permutation = np.random.permutation(len(trainX))
        trainX = trainX[permutation]
        trainY = trainY[permutation]
        trainX = trainX[:inputDataSize]
        trainY = trainY[:inputDataSize]
        trainX,trainY,testX,testY,inputShape = self.__prepareKerasData(trainX,trainY,testX,testY)
        
        neuralNetworkModel = CNNKeras(inputShape)
        neuralNetworkModel.fit(trainX, trainY, epochs)
        result = neuralNetworkModel.evaluate(testX, testY)
        
        '''
        image_index = np.random.randint(0,len(testX))
        print(image_index)
        plt.imshow(testX[image_index].reshape(28, 28),cmap='Greys')
        pred = neuralNetworkModel.predict(testX[image_index].reshape(1, 28, 28, 1))
        print(pred.argmax())
        plt.show()
        '''
        return result

        