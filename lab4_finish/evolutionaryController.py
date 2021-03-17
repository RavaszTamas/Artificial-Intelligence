# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 13:30:00 2020

@author: tamas
"""
import numpy as np
from random import randint, random

class EvolutionaryController():
    
    def __init__(self,repository, matrixSize, populationNumber, probabilityMutation, numberOfIterations):
        self.__matrixSize = matrixSize
        self.__populationNumber = populationNumber
        self.__probabilityMutation = probabilityMutation
        self.__numberOfIterations = numberOfIterations
        self.__population = repository
        self.__interupted = False
        self.__testing = False

    def setTesting(self,value):
        self.__testing = value

    def setMatrixSize(self,newValue):
        self.__matrixSize = newValue
        
    def setPopulationNumber(self,newValue):
        self.__populationNumber = newValue
        
    def setprobabilityMutation(self,newValue):
        self.__probabilityMutation = newValue
        
    def setNumberOfIterations(self,newValue):
        self.__numberOfIterations = newValue

    def interuptProcess(self):
        self.__interupted = True

    def __generateIntialPopulation(self):
        return [self.__generateRandomPermutation() for x in range(self.__populationNumber)]


    def performTests(self):
        self.__testing = True
        resultEA = []
        AverageEA = None
        StandardDevEA = None
        
        for i in range(30):
            resultEA.append(self.startEvolutionary(None)[3])
            print(i)
            if len(resultEA[-1]) != self.__numberOfIterations:
                resultEA[-1] = resultEA[-1] + (self.__numberOfIterations-len(resultEA[-1]))*[0]
            if self.__interupted:
                self.__testing = False
                return
        print("EA done")
        averagesEA =  self.__averageForEachGeneration(resultEA)
        AverageEA = np.mean(resultEA)
        StandardDevEA = np.std(resultEA)
        return (averagesEA,AverageEA,StandardDevEA)
    
    def __averageForEachGeneration(self,resultEA):
        averages = []
        length = len(resultEA)
        for j in range(len(resultEA[0])):
            s = 0
            for i in range(len(resultEA)):
                s += resultEA[i][j]
            averages.append(s/length)
        return averages

    
    def startEvolutionary(self,progress_callback):
        self.__interupted = False
        self.__population.setPopulation(self.__generateIntialPopulation())
        
        bestFitnessResults = []
        
        for i in range(self.__numberOfIterations):

            self.__performIterationEA()
                        
            bestFitnessResults.append(self.__calculateFitness(self.__population.getPopulation()[0]))
            
            if bestFitnessResults[-1] == 0:
                return (self.__calculateFitness(self.__population.getPopulation()[0]),self.__population.getPopulation()[0],i+1,bestFitnessResults)
            
            if self.__interupted == True:
                break
            if i%100 == 0 and not self.__testing:
                progress_callback.emit((self.__calculateFitness(self.__population.getPopulation()[0]),self.__population.getPopulation()[0],i))

        return (self.__calculateFitness(self.__population.getPopulation()[0]),self.__population.getPopulation()[0],i+1,bestFitnessResults)



    
    def __performIterationEA(self):
        
        fitness = self.__calulcateFitnessForPopulation()
        fitness = sorted(fitness, key=lambda x:x[0])
                
        rankedSelection = []
        for i in range(len(self.__population)):
            rankedSelection.append(((len(self.__population)-i)/len(self.__population),fitness[i][1]))


        parents = self.__selectParents(rankedSelection)
        newPopulation  = self.__generateNewPopulation(parents)
        self.__population.setPopulation(newPopulation)
    
    def __calulcateFitnessForPopulation(self):
        fitness = []
        for individual in self.__population.getPopulation():
            fitness.append((self.__calculateFitness(individual),individual))
        return fitness

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


    def __selectParents(self,rankedSelection):
        parents = []
        
        for i in range(len(rankedSelection)):
            if rankedSelection[i][0] >= random():
                parents.append(rankedSelection[i][1])
        return parents

    def __generateNewPopulation(self,parents):
        children = []
        if(len(parents) == 1):
            return parents[:]
        while len(parents) + len(children) < self.__populationNumber:
            i1=randint(0,len(parents)-1)
            i2=randint(0,len(parents)-1)
            if (i1!=i2):
                child = self.__performCrossover(parents[i1], parents[i1])
                child = self.__performMutation(child)
                children.append(child)
        return parents[:] + children[:]

    def __performCrossover(self,firstIndividual,secondIndividual):
            k = randint(0, len(firstIndividual)) 
            
            h = randint(k, len(firstIndividual)) 

            child = firstIndividual[:k] + secondIndividual[k:h] + firstIndividual[h:]

            return child
            
    def __performMutation(self, individual):
        
        if self.__probabilityMutation > random():
            pos = randint(0, len(individual)-1)
            arr = [i for i in range(1,self.__matrixSize+1)]
            individual[pos] = np.random.permutation(arr)

        return individual


    def __generateRandomPermutation(self):
        '''
        Generates a random permutation of size of the matrix

        returns: a matrix containing the permutations
        -------
        '''
        arr = [i for i in range(1,self.__matrixSize+1)]
        return [ np.random.permutation(arr).tolist() for x in range(2*self.__matrixSize)]  
