# -*- coding: utf-8 -*-
"""
Created on Fri May 15 12:24:16 2020

@author: tamas
"""
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, Dropout, Flatten, MaxPooling2D


class CNNKeras():
    
    def __init__(self,input_shape):
        self.__neuralNetworkModel = Sequential()
        self.__neuralNetworkModel.add(Conv2D(28, kernel_size=(3,3),
                                             input_shape=input_shape))
        self.__neuralNetworkModel.add(MaxPooling2D(pool_size=(2, 2)))
        # Flattening the 2D arrays for fully connected layers
        self.__neuralNetworkModel.add(Flatten()) 
        self.__neuralNetworkModel.add(Dense(128, activation=tf.nn.relu))
        self.__neuralNetworkModel.add(Dropout(0.2))
        self.__neuralNetworkModel.add(Dense(10,activation=tf.nn.softmax))
        self.__neuralNetworkModel.compile(optimizer='adam', 
                      loss='sparse_categorical_crossentropy', 
                      metrics=['accuracy'])

    def fit(self,trainData,trainDataResult,epochs):
        self.__neuralNetworkModel.fit(x=trainData,y=trainDataResult,
                                      epochs=epochs)

    def evaluate(self,testX, testY):
        return self.__neuralNetworkModel.evaluate(testX, testY)
    
    def predict(self,X):
        return self.__neuralNetworkModel.predict(X)
    