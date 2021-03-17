# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 14:55:55 2020

@author: tamas
"""
from Domain import Particle
from random import randint, random
import copy 
import numpy as np
from math import exp
class PSOController():
    
    def __init__(self,repository,matrixSize, populationNumber, numberOfIterations,w,c1,c2,neighbourHoodSize):
        self.__population = repository
        self.__matrixSize = matrixSize
        self.__populationNumber = populationNumber
        self.__numberOfIterations = numberOfIterations
        self.__interupted = False
        self.__testing = False
        self.__inertiaCoefficient = w
        self.__socialLearningCoefficient  = c1
        self.__cognitiveLearningCoefficient = c2
        self.__neighbourHoodSize = neighbourHoodSize

    def performTests(self):
        resultPSO = []
        AveragePSO = None
        StandardDevPSO = None

        for i in range(30):
            resultPSO.append(self.startPSO(None)[2])
            print(i)
            if len(resultPSO[-1]) != 1000:
                resultPSO[-1] = resultPSO[-1] + (1000-len(resultPSO[-1]))*[resultPSO[-1][-1]]
            if self.__interupted:
                self.__testing = False
                return
        print("PSO done")

        averagesPSO =  self.__averageForEachGeneration(resultPSO)
        AveragePSO = np.mean(resultPSO)
        StandardDevPSO = np.std(resultPSO)
        return (averagesPSO,AveragePSO,StandardDevPSO)


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

    def interuptProcess(self):
        self.__interupted = True

    def setMatrixSize(self,newValue):
        self.__matrixSize = newValue
        
    def setPopulationNumber(self,newValue):
        self.__populationNumber = newValue
                
    def setNumberOfIterations(self,newValue):
        self.__numberOfIterations = newValue

    def setInertiaCoefficient(self,newValue):
        self.__inertiaCoefficient = newValue

    def setSocialLearningCoefficient(self,newValue):
        self.__socialLearningCoefficient = newValue

    def setCognitiveLearningCoefficient(self,newValue):
        self.__cognitiveLearningCoefficient = newValue

    def setNeighbourHoodSize(self,newValue):
        self.__neighbourHoodSize = newValue

    def startPSO(self,progress_callback):
        self.__interupted = False
        self.__population.setPopulation(self.__generatePSOPopulation())
        
        self.__selectNeighbourHoods()
        bestFitnesses=[]
        startIntertia = self.__inertiaCoefficient
        for i in range(self.__numberOfIterations):
            self.__performPSOIteration()
            currentBest = self.__findBest()
            bestFitnesses.append(self.__population.getPopulation()[currentBest].fitness)
            self.__inertiaCoefficient = startIntertia/(i+1)
            if self.__population.getPopulation()[currentBest].fitness == 0:
                return [self.__population.getPopulation()[currentBest],i,bestFitnesses]
            '''
            arrayToCheckForStuck = [self.__population.getPopulation()[i].fitness for i in range(len(self.__population))]
            if len(set(arrayToCheckForStuck)) == 1:
                break
            '''
            if self.__interupted == True:
                break
            if i%10 == 0 and not self.__testing:
                progress_callback.emit([self.__population.getPopulation()[currentBest],i])

        best = self.__findBest()
        
        return [self.__population.getPopulation()[best],i+1,bestFitnesses]



    def __performPSOIteration(self):
        bestNeighbours = []
        #best neighbour for each particle
        for i in range(len(self.__population)):
            neighbours = self.__population.getNeighbourHood(i)
            bestNeighbours.append(neighbours[0])
            for j in range(1,len(neighbours)):
                if self.__population.getPopulation()[bestNeighbours[i]].fitness > self.__population.getPopulation()[neighbours[j]].fitness:
                    bestNeighbours[i] = copy.deepcopy(neighbours[j])
        '''
        for i in range(len(bestNeighbours)):
            print(bestNeighbours[i])
            print(self.__population.getPopulation()[bestNeighbours[i]].fitness)
            print(len(self.__population.getPopulation()[bestNeighbours[i]].velocity))
            print(self.__neighbourHoodSize)
            print(self.__population.getNeighbourHood(i))
            for j in range(self.__neighbourHoodSize):
                print((self.__population.getPopulation()[self.__population.getNeighbourHood(i)[j]].fitness,self.__population.getNeighbourHood(i)[j]),end=", ")
            print()
        '''
        '''
        asd = []    
        #asda= []
        for i in range(len(self.__population)):
            #print(bestNeighbours[i])
            #print(self.__population.getPopulation()[bestNeighbours[i]].fitness)
            asd.append(self.__population.getPopulation()[i].fitness)
            #.append(bestNeighbours[i])
        print(len(set(asd)))
        #print(asda)
        print(asd)
        '''



        for i in range(len(self.__population)):
            for j in range(len(self.__population.getPopulation()[i].velocity)):
                newVelocity = self.__inertiaCoefficient * self.__population.getPopulation()[i].velocity[j]
                newVelocity = newVelocity + self.__socialLearningCoefficient * random() * self.__permutationsDistance(self.__population.getPopulation()[bestNeighbours[i]].getPosition()[j],self.__population.getPopulation()[i].getPosition()[j])
                                                                                                               
                newVelocity = newVelocity + self.__cognitiveLearningCoefficient * random() * self.__permutationsDistance(self.__population.getPopulation()[i].getBestPosition()[j],self.__population.getPopulation()[i].getPosition()[j])
                self.__population.getPopulation()[i].velocity[j] = copy.deepcopy(newVelocity)
        
        for i in range(len(self.__population)):
            for j in range(len(self.__population.getPopulation()[i].velocity)):
                if random() < self.__sigmoid(self.__population.getPopulation()[i].velocity[j]):
                    self.__population.getPopulation()[i].setGene(j,self.__population.getPopulation()[bestNeighbours[i]].getPosition()[j])
            self.__population.getPopulation()[i].evaluateNewFitness()

    def __selectNeighbourHoods(self):
        if(self.__neighbourHoodSize > len(self.__population)):
            self.__neighbourHoodSize = len(self.__population)
            
        for i in range(len(self.__population)):
            localNeighbours=[]
            for j in range(self.__neighbourHoodSize):
                if self.__neighbourHoodSize == len(self.__population):
                    localNeighbours = [i for i in range(self.__neighbourHoodSize)]
                    localNeighbours.remove(i)
                else:
                    x=randint(0, len(self.__population)-1)
                    while x in localNeighbours or x == i:
                        x=randint(0, len(self.__population)-1)
                    localNeighbours.append(x)
            if len(localNeighbours) != len(set(localNeighbours)):
                raise ValueError("Invalid neighbourhood")
            self.__population.setNeighbourHood(i,localNeighbours)

    def __generatePSOPopulation(self):
        return [ Particle(self.__matrixSize) for i in range(self.__populationNumber)]


    def __findBest(self):
        best = 0
        for i in range(1, len(self.__population)):
            if self.__population.getPopulation()[i].fitness < self.__population.getPopulation()[best].fitness:
                best = i
        return best
    
    def __sigmoid(self, value):
        return 1 / (1 + exp(-value))# slide 20

    def __permutationsDistance(self, firstPermutation, secondPermutations):
        distance = 0
        for i in range(len(firstPermutation)):
            distance += abs(firstPermutation[i] - secondPermutations[i])
        return distance