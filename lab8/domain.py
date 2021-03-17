# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 20:19:41 2020

@author: tamas
"""
import numpy as np
from random import random
from copy import deepcopy
def linear_function(x):
    return (1/100)*x + 3


def derivative_linear(x):
    return 1/100

def identical(x):
    return x

def dIdentical(x):
    return 1



'''
class Neuron:
    def __init__(self, noOfInputs, activationFunction):
        self.noOfInputs = noOfInputs
        self.activationFunction = activationFunction
        self.weights = [random() for i in range(self.noOfInputs)]
        self.output = 0
        
    def setWeights(self, newWeights):
        self.weights = newWeights
        
    def fireNeuron(self, inputs):
        u = sum([x*y for x,y in zip(inputs,self.weights)])
        self.output = self.activationFunction(u)
        return(self.output)
        
    def __str__(self):
        return str(self.weights)
        
class Layer:
    def __init__(self, noOfInputs, activationFunction, noOfNeurons):
        self.noOfNeurons = noOfNeurons
        self.neurons = [Neuron(noOfInputs, activationFunction) for i in 
                      range(self.noOfNeurons)]
        
    
    def forward(self, inputs):
        for x in self.neurons:
            x.fireNeuron(inputs)
        return([x.output for x in self.neurons])
        
    def __str__(self):
        s = ''
        for i in range(self.noOfNeurons):
            s += ' n '+str(i)+' '+str(self.neurons[i])+'\n'
        return s
        
class FirstLayer(Layer):
    def __init__(self, noOfNeurons, bias = False):
        if bias :
            noOfNeurons = noOfNeurons + 1
        Layer.__init__(self, 1, identical, noOfNeurons)
        for x in self.neurons:
            x.setWeights([1])
            
    def forward(self, inputs):
        for i in range(len(self.neurons)):
            self.neurons[i].fireNeuron([inputs[i]])
        return([x.output for x in self.neurons])
        # return inputs
        
class Network:
    def __init__(self, structure, activationFunction, derivate, bias = False):
        self.activationFunction = activationFunction
        self.derivate = derivate
        self.bias = bias
        self.structure = structure[:]
        self.noLayers = len(self.structure)
        self.layers = [FirstLayer(self.structure[0], bias)]
        for i in range(1, len(self.structure)):
            self.layers = self.layers + [Layer(self.structure[i-1],
                            activationFunction, self.structure[i])]
        
    def feedForward(self, inputs):
        self.signal = inputs[:]
        if self.bias:
            self.signal.append(1)
        for l in self.layers:
            self.signal = l.forward(self.signal)
        return self.signal

    def backPropag(self, loss, learnRate):
        err = loss[:]
        delta = []
        currentLayer = self.noLayers-1
        newConfig = Network(self.structure, self.activationFunction, self.derivate, self.bias)
        # last layer
        for i in range(self.structure[-1]):
            delta.append(err[i]*self.derivate(self.layers[-1].neurons[i].output))
            for r in range(self.structure[currentLayer-1]):
                newConfig.layers[-1].neurons[i].weights[r] = self.layers[-1].neurons[i].weights[r] + learnRate*delta[i]*self.layers[currentLayer-1].neurons[r].output
        
        #propagate the errors layer by layer
        for currentLayer in range(self.noLayers-2,0,-1):
            
            currentDelta = []
            for i in range(self.structure[currentLayer]):
                currentDelta.append(self.derivate(self.layers[currentLayer].neurons[i].output)*sum([self.layers[currentLayer+1].neurons[j].weights[i]*delta[j] for j in range(self.structure[currentLayer+1])]))
            
            delta = currentDelta [:]
            for i in range(self.structure[currentLayer]):
                for r in range(self.structure[currentLayer-1]):
                    newConfig.layers[currentLayer].neurons[i].weights[r] = self.layers[currentLayer].neurons[i].weights[r] + learnRate*delta[i]*self.layers[currentLayer-1].neurons[r].output
        self.layers=deepcopy(newConfig.layers)
        
        
    def computeLoss(self, u, t):
        loss = []
        out = self.feedForward(u)
        for i in range(len(t)):
            loss.append(t[i]-out[i])
        return loss[:]
    
    def __str__(self):
        s = ''
        for i in range(self.noLayers):
            s += ' l '+str(i)+' :'+str(self.layers[i])
        return s

'''

class NeuralNetwork:
    def __init__(self,x,y,hidden,activationFunction,derivateOfActivation):
        self.activationFunction = activationFunction
        self.derivateOfActivation = derivateOfActivation
        self.input = x
        self.weightsFirstLayerIn = np.random.rand(self.input.shape[1],hidden)
        self.weightsFirstLayerOut = np.random.rand(hidden,1)
        self.expected = y
        self.output = np.zeros(self.expected.shape)
        self.loss = []
        self.normalizeInput()
    
    def setInput(self,newInput):
        self.input = newInput
        self.normalizeInput()
        
    def getOutput(self):
        return self.output
    
    def getLoss(self):
        return self.loss

    def normalizeInput(self):
        
        newInput = np.empty((0,self.input.shape[1]),int)
        xMin = np.amin(self.input)
        xMax = np.amax(self.input)
        #print((xMin,xMax))
        #print(newInput.shape)
        for X in self.input:
            xMin = np.amin(X)
            xMax = np.amax(X)
            xNew = (X - xMin)/(xMax-xMin)
            #print(xNew)
            #print(xNew)
            newInput = np.append(newInput,[xNew],axis=0)
        #print(newInput)
        self.input = newInput
    def feedForward(self):
        self.layer1 = self.activationFunction(np.dot(self.input,self.weightsFirstLayerIn))
        #print(self.layer1)
        self.output = self.activationFunction(np.dot(self.layer1,self.weightsFirstLayerOut))
        #print(self.output)
        #input("forward")
    def backprop(self,learning_rate):
        d_weights2 = np.dot(self.layer1.T,(2*(self.expected - self.output) * self.derivateOfActivation(self.output)))
        #print(d_weights2)
   
        d_weights1 = np.dot(self.input.T,(np.dot(2*(self.expected-self.output) * self.derivateOfActivation(self.output),
                                                 self.weightsFirstLayerOut.T
                                                 ) * self.derivateOfActivation(self.layer1)))
        #print(d_weights1)
        self.weightsFirstLayerIn += learning_rate * d_weights1
        self.weightsFirstLayerOut += learning_rate * d_weights2

        self.loss.append(sum((self.expected - self.output)**2))
        #print(self.loss[-1])
        #input("weights")


