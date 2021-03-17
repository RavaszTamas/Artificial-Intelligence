# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 13:49:24 2020

@author: tamas
"""
import numpy as np
import copy

class Individual():
    
    def __init__(self,dimension):
        self.__matrixSize = dimension
        self.__position = self.__generateRandomPermutation()
        self.__fitness = self.calculateFitness()
        
    def __generateRandomPermutation(self):
        '''
        Generates a random permutation of size of the matrix

        returns: a matrix containing the permutations
        -------
        '''
        arr = [i for i in range(1,self.__matrixSize+1)]
        return [ np.random.permutation(arr) for x in range(2*self.__matrixSize)]  

    def calculateFitness(self,individual):
        
        return self.__numberOfNonUnique(individual) + self.__checkColumnsForPermutations(individual)

    def __numberOfNonUnique(self,matrixToCheck):
        matrix = []
        
        for i in range(self.__matrixSize):
            for j in range(self.__matrixSize):
                matrix.append((matrixToCheck[i][j],matrixToCheck[i+self.__matrixSize][j]))
        return self.__matrixSize**2 - len(set(matrix))

    def __checkColumnsForPermutations(self,matrixToCheck):
        error = 0
        for j in range(self.__matrixSize):
            firstMatrix = []
            secondMatrix = []
            for i in range(self.__matrixSize):
                firstMatrix.append(matrixToCheck[i][j])
                secondMatrix.append(matrixToCheck[i+self.__matrixSize][j])
            error += self.__matrixSize - len(set(firstMatrix))
            error += self.__matrixSize - len(set(secondMatrix))
        return error


class Particle():
    def __init__(self,dimension):
        self.__matrixSize = dimension
        self.__position = self.__generateRandomPermutation()
        self.evaluate()
        self.velocity = [0 for i in range(self.__matrixSize*2)]
        
        self.__bestPosition = copy.deepcopy(self.__position)
        self.__bestFitness = self.__fitness
    def __generateRandomPermutation(self):
        '''
        Generates a random permutation of size of the matrix

        returns: a matrix containing the permutations
        -------
        '''
        arr = [i for i in range(1,self.__matrixSize+1)]
        return [ np.random.permutation(arr) for x in range(2*self.__matrixSize)]  

    def evaluate(self):
        self.__fitness = self.calculateFitness(self.__position)
        
    def calculateFitness(self,individual):
        
        return self.__numberOfNonUnique(individual) + self.__checkColumnsForPermutations(individual)

        
    def __numberOfNonUnique(self,matrixToCheck):
        matrix = []
        
        for i in range(self.__matrixSize):
            for j in range(self.__matrixSize):
                matrix.append((matrixToCheck[i][j],matrixToCheck[i+self.__matrixSize][j]))
        return self.__matrixSize**2 - len(set(matrix))

    def __checkColumnsForPermutations(self,matrixToCheck):
        error = 0
        for j in range(self.__matrixSize):
            firstMatrix = []
            secondMatrix = []
            for i in range(self.__matrixSize):
                firstMatrix.append(matrixToCheck[i][j])
                secondMatrix.append(matrixToCheck[i+self.__matrixSize][j])
            error += self.__matrixSize - len(set(firstMatrix))
            error += self.__matrixSize - len(set(secondMatrix))
        return error


    def getPosition(self):
        return self.__position
    
    def getBestPosition(self):
        return self.__bestPosition

    def setGene(self,index,newRow):
        self.__position[index] = copy.deepcopy(newRow)

    @property
    def position(self):
        """ getter for pozition """
        return self.__position
    @property
    def fitness(self):
        """ getter for fitness """
        return self.__fitness
    @property
    def bestPosition(self):
        """ getter for best pozition """
        return self.__bestPosition

    @property
    def bestFitness(self):
        """getter for best fitness """
        return self.__bestFitness
    
    @position.setter
    def position(self, newPosition):
        self.__position=copy.deepcopy(newPosition)
        # automatic evaluation of particle's fitness
        self.evaluate()
        # automatic update of particle's memory
        if (self.__fitness<self.__bestFitness):
            self.__bestPosition = self.__position
            self.__bestFitness  = self.__fitness
    
    
    def evaluateNewFitness(self):
        self.evaluate()
        # automatic update of particle's memory
        if (self.__fitness<self.__bestFitness):
            self.__bestPosition = self.__position
            self.__bestFitness  = self.__fitness

    
    def __str__(self):
        s=""
        s+=str(self.__position) + "\n"
        s+=str(self.velocity) + "\n"
        s+=str(self.__bestPosition) + "\n"
        s+=str(self.__bestFitness) + "\n"
        return s
    
    def __repr__(self):
        return str(self)