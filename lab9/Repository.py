# -*- coding: utf-8 -*-
"""
Created on Thu May 14 00:17:09 2020

@author: tamas
"""
import numpy as np

import codecs

from keras.datasets import mnist
import tensorflow as tf


class Repository():
    
    def get_int(self,b):
        return int(codecs.encode(b,'hex'),16)
    
    def __init__(self,filename="training/train-images.idx3-ubyte",labels="training/train-labels.idx1-ubyte",
                 testFilename="test/t10k-images.idx3-ubyte", testLabels="test/t10k-labels.idx1-ubyte"):
            self.__filename = filename
            self.__labels = labels
            self.__testFilename = testFilename
            self.__testLabels = testLabels

    def getTrainingDataKeras(self):
        
        
        (trainX, trainy), (testX, testy) = tf.keras.datasets.mnist.load_data() #mnist.load_data()
        return trainX,trainy,testX,testy

    def getTrainingData(self):
        parsedImages = None
        parsedLabels = None
        with open(self.__filename, 'rb') as f:
            data = f.read()
            length = self.get_int(data[4:8])
            num_rows = self.get_int(data[8:12])
            num_cols = self.get_int(data[12:16])
            parsedImages = np.frombuffer(data,dtype = np.uint8, offset=16)
            parsedImages = parsedImages.reshape(length,num_rows,num_cols)

        with open(self.__labels, 'rb') as f:
            data = f.read()
            
            length = self.get_int(data[4:8])
            parsedLabels = np.frombuffer(data,dtype = np.uint8, offset=8)
            parsedLabels = parsedLabels.reshape(length)
            
        return parsedImages,parsedLabels
    
    
    def getTestData(self):
        parsedImages = None
        parsedLabels = None
        with open(self.__testFilename, 'rb') as f:
            data = f.read()
            length = self.get_int(data[4:8])
            num_rows = self.get_int(data[8:12])
            num_cols = self.get_int(data[12:16])
            parsedImages = np.frombuffer(data,dtype = np.uint8, offset=16)
            parsedImages = parsedImages.reshape(length,num_rows,num_cols)

        with open(self.__testLabels, 'rb') as f:
            data = f.read()
            
            length = self.get_int(data[4:8])
            parsedLabels = np.frombuffer(data,dtype = np.uint8, offset=8)
            parsedLabels = parsedLabels.reshape(length)
            
        return parsedImages,parsedLabels