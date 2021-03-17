# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 14:32:53 2020

@author: tamas
"""
import copy 
import numpy as np

class HillClimbingController():
    
    def __init__(self,matrixSize, numberOfIterations):
        self.__matrixSize = matrixSize
        self.__numberOfIterations = numberOfIterations
        self.__interupted = False
        self.__testing = False

    def __averageForEachGeneration(self,resultEA):
        averages = []
        length = len(resultEA)
        for j in range(len(resultEA[0])):
            s = 0
            for i in range(len(resultEA)):
                s += resultEA[i][j]
            averages.append(s/length)
        return averages


    def setTesting(self,value):
        self.__testing = value

    def performTests(self):
        resultHillClimbing = []
        AverageHillClimbing = None
        StandardDevHillClimbing = None
        
        for i in range(30):
            resultHillClimbing.append(self.startHillClimbing(None)[3])
            print(i)
            if len(resultHillClimbing[-1]) != self.__numberOfIterations:
                resultHillClimbing[-1] = resultHillClimbing[-1] + (self.__numberOfIterations-len(resultHillClimbing[-1]))*[0]
            if self.__interupted:
                self.__testing = False
                return
        print("HC done")
        averagesHillClimbing =  self.__averageForEachGeneration(resultHillClimbing)
        AverageHillClimbing = np.mean(resultHillClimbing)
        StandardDevHillClimbing = np.std(resultHillClimbing)
        return(averagesHillClimbing,AverageHillClimbing,StandardDevHillClimbing)

    def interuptProcess(self):
        self.__interupted = True
        
    def setMatrixSize(self,newValue):
        self.__matrixSize = newValue
                        
    def setNumberOfIterations(self,newValue):
        self.__numberOfIterations = newValue

    def startHillClimbing(self,progress_callback):
        self.__interupted = False
        current = self.__generateRandomPermutation()
        prevFitness  = self.__calculateFitness(current) 
        fitnessForEachIteration = []
        
        visited = [copy.deepcopy(current)]
        
        
        globalBest = current
        globalBestFitness = self.__calculateFitness(globalBest)
        
        for i in range(self.__numberOfIterations):

            best = self.__findTheBestNeighbour(copy.deepcopy(current))
            currentFitness = self.__calculateFitness(current)
            bestFitness = self.__calculateFitness(best)
            
            if currentFitness > bestFitness:
                current = best
                currentFitness = bestFitness
                if globalBestFitness > currentFitness:
                    globalBest = current
                    globalBestFitness = currentFitness

            ''' If no update on the fitness that means we are on a peak, or on a plain, new start needed'''
            if prevFitness == currentFitness:
                current = self.__generateRandomPermutation()
                numOfTries = 0
                while current in visited and numOfTries <100:
                    current = self.__generateRandomPermutation()
                    numOfTries+=1
                visited.append(copy.deepcopy(current))
                prevFitness  = self.__calculateFitness(current) 
            
            prevFitness = currentFitness
            fitnessForEachIteration.append(globalBestFitness)
            if self.__calculateFitness(current) == 0:
                return (0,current,i,fitnessForEachIteration)
            
            
            if self.__interupted == True:
                break
            if i%10 == 0 and not self.__testing:
                progress_callback.emit((globalBestFitness,globalBest,i))

        return (globalBestFitness,globalBest,i+1,fitnessForEachIteration)        

    def __generateRandomPermutation(self):
        '''
        Generates a random permutation of size of the matrix

        returns: a matrix containing the permutations
        -------
        '''
        arr = [i for i in range(1,self.__matrixSize+1)]
        return [ np.random.permutation(arr).tolist() for x in range(2*self.__matrixSize)]  

    def __calculateFitness(self,individual):
        
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


    def __findTheBestNeighbour(self,current):
        result = None
        for i in range(len(current)):
            for j in range(len(current[i])):
                for k in range(j+1,len(current[i])):
                    empty = current[i][j]
                    current[i][j] = current[i][k]
                    current[i][k] = empty
                    if result == None:
                        result = copy.deepcopy(current)
                    if self.__calculateFitness(current) < self.__calculateFitness(result):
                        result = copy.deepcopy(current)
                    empty = current[i][j]
                    current[i][j] = current[i][k]
                    current[i][k] = empty

        return result
