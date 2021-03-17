# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 13:49:19 2020

@author: tamas
"""
import numpy as np
from random import randint, random
import copy 
from Domain import Particle
import math
class Controller():
    
    def __init__(self, matrixSize, population, probabilityMutation, numberOfIterations,w,c1,c2):
        self.__matrixSize = matrixSize
        self.__population = population
        self.__probabilityMutation = probabilityMutation
        self.__numberOfIterations = numberOfIterations
        self.__interupted = False
        self.__testing = False
        self.__inertiaCoefficient = w
        self.__socialLearningCoefficient  = c1
        self.__cognitiveLearningCoefficient = c2
        
    def performTests(self,progress_callback):
        self.__testing = True
        resultEA = []
        AverageEA = None
        StandardDevEA = None
        
        for i in range(30):
            resultEA.append(self.startEvolutionary(None)[3])
            print(i)
            if len(resultEA[-1]) != 1000:
                resultEA[-1] = resultEA[-1] + (1000-len(resultEA[-1]))*[0]
            if self.__interupted:
                self.__testing = False
                return
        print("EA done")
        averagesEA =  self.__averageForEachGeneration(resultEA)
        AverageEA = np.mean(resultEA)
        StandardDevEA = np.std(resultEA)
    
        resultHillClimbing = []
        AverageHillClimbing = None
        StandardDevHillClimbing = None
        
        for i in range(30):
            resultHillClimbing.append(self.startHillClimbing(None)[3])
            print(i)
            if len(resultHillClimbing[-1]) != 1000:
                resultHillClimbing[-1] = resultHillClimbing[-1] + (1000-len(resultHillClimbing[-1]))*[0]
            if self.__interupted:
                self.__testing = False
                return
        print("HC done")

        averagesHillClimbing =  self.__averageForEachGeneration(resultHillClimbing)
        AverageHillClimbing = np.mean(resultHillClimbing)
        StandardDevHillClimbing = np.std(resultHillClimbing)


        resultPSO = []
        AveragePSO = None
        StandardDevPSO = None

        for i in range(30):
            resultPSO.append(self.startPSO(None)[2])
            print(i)
            if len(resultPSO[-1]) != 1000:
                resultPSO[-1] = resultPSO[-1] + (1000-len(resultPSO[-1]))*[0]
            if self.__interupted:
                self.__testing = False
                return
        print("PSO done")

        averagesPSO =  self.__averageForEachGeneration(resultPSO)
        AveragePSO = np.mean(resultPSO)
        StandardDevPSO = np.std(resultPSO)

        self.__testing = False
        return ((averagesEA,AverageEA,StandardDevEA)
                ,(averagesHillClimbing,AverageHillClimbing,StandardDevHillClimbing)
                ,(averagesPSO,AveragePSO,StandardDevPSO))

        
    
    def __averageForEachGeneration(self,resultEA):
        averages = []
        length = len(resultEA)
        for j in range(len(resultEA[0])):
            s = 0
            for i in range(len(resultEA)):
                s += resultEA[i][j]
            averages.append(s/length)
        return averages
    
    def interuptProcess(self):
        self.__interupted = True
    
    def startPSO(self,progress_callback):
        self.__interupted = False
        PSOPopulation = self.__generatePSOPopulation()
        sizeOfNeighbourhood = 10
        
        neighbourHoods = self.__selectNeighbourHoods(PSOPopulation,sizeOfNeighbourhood)
        bestFitnesses=[]
        for i in range(self.__numberOfIterations):
            PSOPopulation = self.__performPSOIteration(PSOPopulation,neighbourHoods,self.__socialLearningCoefficient,self.__cognitiveLearningCoefficient,self.__inertiaCoefficient/(i+1))
            currentBest = 0
            
            for j in range(1,len(PSOPopulation)):
                if PSOPopulation[j].fitness < PSOPopulation[currentBest].fitness:
                    currentBest = j

            bestFitnesses.append(PSOPopulation[currentBest].fitness)
            print(PSOPopulation[0].position)
            '''
            print(PSOPopulation[currentBest].position)
            for elem in PSOPopulation[currentBest].velocity:
                print(["%0.2f" % i for i in elem],end=",")
            print(currentBest,end="\n\n")
            '''
            if PSOPopulation[currentBest].fitness == 0:
                return [PSOPopulation[currentBest],i,bestFitnesses]
            
            if self.__interupted == True:
                break
            if i%10 == 0 and not self.__testing:
                progress_callback.emit([PSOPopulation[currentBest],i])

        best = 0
        for j in range(1, len(PSOPopulation)):
            if (PSOPopulation[j].fitness<PSOPopulation[best].fitness):
                best = j
        
        return [PSOPopulation[best],i+1,bestFitnesses]
        
    def __performPSOIteration(self,population,neighbourHoods,c1,c2,w):
        bestNeighbours = []
        
        #best neighbour for each particle
        for i in range(len(population)):
            bestNeighbours.append(neighbourHoods[i][0])
            for j in range(1,len(neighbourHoods[i])):
                if population[bestNeighbours[i]].fitness > population[neighbourHoods[i][j]].fitness:
                    bestNeighbours[i] = neighbourHoods[i][j]
        
        
                
        
        for i in range(len(population)):
            for j in range(len(population[i].velocity)):
                for k in range(len(population[i].velocity[j])):
                    newVelocity = w * population[i].velocity[j][k]
                    newVelocity = newVelocity + c1 * random() * (population[bestNeighbours[i]].position[j][k] - population[i].position[j][k])
                    newVelocity = newVelocity + c2 * random() * (population[i].bestPosition[j][k] - population[i].position[j][k])
                    
                    population[i].velocity[j][k] = newVelocity


        for i in range(len(population)):
            newPosition = []
            for j in range(len(population[i].velocity)):
                newGene = []
                for k in range(len(population[i].velocity[j])):
                    newGene.append(int(np.clip(round(population[i].position[j][k]+population[i].velocity[j][k]),1,self.__matrixSize)))
                newPosition.append(newGene)
            population[i].position = newPosition
        return population
    
    def __selectNeighbourHoods(self,population,sizeOfNeighbourhood):
        if(sizeOfNeighbourhood > len(population)):
            sizeOfNeighbourhood = len(population)
            
        newNeighbourHoods=[]
        for i in range(len(population)):
            localNeighbours=[]
            for j in range(sizeOfNeighbourhood):
                x=randint(0, len(population)-1)
                while x in localNeighbours and x == i:
                    x=randint(0, len(population)-1)
                localNeighbours.append(x)
            newNeighbourHoods.append(localNeighbours.copy())
        return newNeighbourHoods

        
    def __generatePSOPopulation(self):
        return [ Particle(self.__matrixSize) for i in range(self.__population)]
    
    def startHillClimbing(self,progress_callback):
        self.__interupted = False
        current = self.__generateRandomPermutation()
        prevFitness  = self.__calculateFitness(current) 
        fitnessForEachIteration = [prevFitness]
        
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
    
    def __generateIntialPopulation(self):
        return [self.__generateRandomPermutation() for x in range(self.__population)]

    
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
                    
    def __printMatrix(self,matrix):
        for i in range(len(matrix)//2):
            for j in range(len(matrix)//2):
                print("("+str(matrix[i][j]) +","+str(matrix[i+len(matrix)//2][j])+") ",end="")
            print()
        print()
        
    def startEvolutionary(self,progress_callback):
        self.__interupted = False
        populationEntities = self.__generateIntialPopulation()
        bestFitnessResults = []
        for i in range(self.__numberOfIterations):

            populationEntities = self.__performIterationEA(populationEntities)
            
            if len(populationEntities) == 1 and len(populationEntities[0]) == 2:
                bestFitnessResults.append(0)
                
                return (populationEntities[0][0],populationEntities[0][1],i+1,bestFitnessResults)
            
            bestFitnessResults.append(self.__calculateFitness(populationEntities[0]))
            
            if self.__interupted == True:
                break
            if i%100 == 0 and not self.__testing:
                progress_callback.emit((self.__calculateFitness(populationEntities[0]),populationEntities[0],i))

        return (self.__calculateFitness(populationEntities[0]),populationEntities[0],i+1,bestFitnessResults)

    def __performIterationEA(self,population):
        
        fitness = self.__calulcateFitnessForPopulation(population)
        fitness = sorted(fitness, key=lambda x:x[0])
        
        if fitness[0][0] == 0:
            return [fitness[0]]
        
        rankedSelection = []
        for i in range(len(population)):
            rankedSelection.append(((len(population)-i)/len(population),fitness[i][1]))


        parents = self.__selectParents(rankedSelection)
        newPopulation  = self.__generateNewPopulation(parents)
        return newPopulation

    def __generateNewPopulation(self,parents):
        children = []
        if(len(parents) == 1):
            return parents[:]
        while len(parents) + len(children) < self.__population:
            i1=randint(0,len(parents)-1)
            i2=randint(0,len(parents)-1)
            if (i1!=i2):
                child = self.__performCrossover(parents[i1], parents[i1])
                child = self.__performMutation(child)
                children.append(child)
        return parents[:] + children[:]
    
    def __selectParents(self,rankedSelection):
        parents = []
        
        for i in range(len(rankedSelection)):
            if rankedSelection[i][0] >= random():
                parents.append(rankedSelection[i][1])
        return parents
    
    def __calulcateFitnessForPopulation(self,population):
        fitness = []
        for individual in population:
            fitness.append((self.__calculateFitness(individual),individual))
        return fitness

    def __calculateFitness(self,individual):
        
        return self.__numberOfNonUnique(individual) + self.__checkColumnsForPermutations(individual)

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
    
    def __numberOfNonUnique(self,matrixToCheck):
        matrix = []
        
        for i in range(self.__matrixSize):
            for j in range(self.__matrixSize):
                #print("("+str(matrixToCheck[i][j]) +","+str(matrixToCheck[i+self.__matrixSize][j])+") ",end="")
                matrix.append((matrixToCheck[i][j],matrixToCheck[i+self.__matrixSize][j]))
        return self.__matrixSize**2 - len(set(matrix))

    def __checkColumnsForPermutations(self,matrixToCheck):
        error = 0
        for j in range(self.__matrixSize):
            firstMatrix = []
            secondMatrix = []
            for i in range(self.__matrixSize):
                #print("("+str(matrix[i][j]) +","+str(matrix[i+self.__matrixSize][j])+") ",end="")
                firstMatrix.append(matrixToCheck[i][j])
                secondMatrix.append(matrixToCheck[i+self.__matrixSize][j])
            #print(firstMatrix,end=" ")
            #print(secondMatrix)
            #print(set(firstMatrix),end=" ")
            #print(set(secondMatrix))

            error += self.__matrixSize - len(set(firstMatrix))
            error += self.__matrixSize - len(set(secondMatrix))
        return error






