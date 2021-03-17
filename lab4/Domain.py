# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 13:49:24 2020

@author: tamas
"""
import numpy as np
import copy
from random import randint, random, choice
class Ant():
        
    def __init__(self,matrixSize):
        self.__size = matrixSize
        self.__path = [[randint(0,self.__size-1)] for j in range(2*self.__size)]
        self.__currentPermutation = 0
        
    def getSize(self):
        return self.__size
        
    def getPath(self):
        return self.__path
        
    def nextMoves(self):
        moves = []

        for i in range(self.__size):
            if i not in self.__path[self.__currentPermutation]:
                moves.append(i)
        
        return moves
        
    def addMove(self, q0, trace, alpha,beta):
        p = [0 for i in range(self.__size)]
        nextSteps= copy.deepcopy(self.nextMoves())
        if (len(nextSteps) == 0):
            return False
        for i in nextSteps:
            p[i] = 1
        p=[(p[i]**beta)*(trace[self.__currentPermutation][self.__path[self.__currentPermutation][-1]][i]**alpha) for i in range(len(p))]
        
        if random() < q0:
            p = [ [i, p[i]] for i in range(len(p))]
            p = max(p, key=lambda a: a[1])
            self.__path[self.__currentPermutation].append(p[0])
        else:
            s = sum(p)
            if (s==0):
                return choice(nextSteps)
            p = [ p[i]/s for i in range(len(p))]
            p = [ sum(p[0:i+1]) for i in range(len(p))]
            r=random()
            i=0
            while (r > p[i]):
                i=i+1
            self.__path[self.__currentPermutation].append(i)
        if len(self.__path[self.__currentPermutation]) == self.__size:
            self.__currentPermutation += 1
        return True
    
    def fitness(self):
        '''
        if self.__currentPermutation != self.__size*2:
            raise IndexError("Ant unfinished")
            
        if len(self.__path[-1]) != self.__size:
            raise IndexError("Ant unfinished")
        '''
        return self.__numberOfNonUnique() + self.__checkColumnsForPermutations()
        

    def __numberOfNonUnique(self):
        matrix = []
        
        for i in range(self.__size):
            for j in range(self.__size):
                matrix.append((self.__path[i][j],self.__path[i+self.__size][j]))
        return self.__size**2 - len(set(matrix))

    def __checkColumnsForPermutations(self):
        error = 0
        for j in range(self.__size):
            firstMatrix = []
            secondMatrix = []
            for i in range(self.__size):
                firstMatrix.append(self.__path[i][j])
                secondMatrix.append(self.__path[i+self.__size][j])
            error += self.__size - len(set(firstMatrix))
            error += self.__size - len(set(secondMatrix))
        return error


class ACOProblem():
     
    def __init__(self,matrixSize,numberOfIterations,numberOfAnts,alpha,beta,rho,q0):
        self.__matrixSize = matrixSize
        self.__numberOfIterations = numberOfIterations
        self.__numberOfAnts = numberOfAnts
        self.__alpha = alpha
        self.__beta = beta
        self.__rho = rho
        self.__q0 = q0

    def loadProblem(self):
        return [self.__matrixSize,self.__numberOfIterations,self.__numberOfAnts,self.__alpha,self.__beta,self.__rho,self.__q0]

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