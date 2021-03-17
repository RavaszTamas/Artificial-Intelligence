"""
@author: tamas
"""
import copy 
import numpy as np
from Domain import Ant
class ACOController():
    
    def __init__(self,acoProblem):
        self.__problem = acoProblem
        self.__loadData()
    
    def __loadData(self):
        parameters = self.__problem.loadProblem()
        self.__matrixSize = parameters[0]
        self.__numberOfIterations = parameters[1]
        self.__numberOfAnts = parameters[2]
        self.__alpha = parameters[3]
        self.__beta = parameters[4]
        self.__rho = parameters[5]
        self.__q0 = parameters[6]
        self.__interupted = False
        self.__testing = False
        self.__trace = []

    
    def performTests(self):
        self.__testing = True
        resultACO = []
        AverageACO = None
        StandardDevACO = None
        print("ACO start")
        for i in range(30):
            resultACO.append(self.startACO(None)[2])
            print(i)
            if len(resultACO[-1]) != self.__numberOfIterations:
                resultACO[-1] = resultACO[-1] + (self.__numberOfIterations-len(resultACO[-1]))*[resultACO[-1][-1]]
            if self.__interupted:
                self.__testing = False
                return
        print("ACO done")
        averagesACO =  self.__averageForEachGeneration(resultACO)
        AverageACO = np.mean(resultACO)
        StandardDevACO = np.std(resultACO)
        return (averagesACO,AverageACO,StandardDevACO)

    def __averageForEachGeneration(self,resultACO):
        averages = []
        length = len(resultACO)
        for j in range(len(resultACO[0])):
            s = 0
            for i in range(len(resultACO)):
                s += resultACO[i][j]
            averages.append(s/length)
        return averages

    def setTesting(self,value):
        self.__testing = value
    
    def setProblem(self,newProblem):
        self.__problem = newProblem
        self.__loadData()
    '''
    def setMatrixSize(self,newValue):
        self.__matrixSize = newValue
    def setNumberOfAnts(self,newValue):
        self.__numberOfAnts = newValue
    def setNumberOfIterations(self,newValue):
        self.__numberOfIterations = newValue
    def setAlpha(self,newValue):
        self.__alpha = newValue
    def setBeta(self,newValue):
        self.__beta = newValue
    def setRho(self,newValue):
        self.__rho = newValue
    def setQ0(self,newValue):
        self.__q0 = newValue
        
        
    '''
    def interuptProcess(self):
        self.__interupted = True

    def startACO(self,progress_callback):
        sol=None
        self.__interupted = False
        
        self.__trace = [[[1 for i in range(self.__matrixSize)] for j in range(self.__matrixSize)] for k in range(2*self.__matrixSize)]

        bestSol = self.__performACOIteration()
        
        bestFitnesses = [bestSol.fitness()]
        bestForEachIter = [bestSol.fitness()]
        if bestFitnesses[0] == 0:
            return (bestSol,1,bestFitnesses,bestForEachIter)
        for i in range(self.__numberOfIterations-1):
            sol = self.__performACOIteration()
            if sol.fitness()<=bestSol.fitness():
                bestSol=copy.deepcopy(sol)
                if bestSol.fitness() == 0:
                    bestForEachIter.append(sol.fitness())
                    bestFitnesses.append(bestSol.fitness())
                    return (bestSol,i+2,bestFitnesses,bestForEachIter)
            bestForEachIter.append(sol.fitness())
            bestFitnesses.append(bestSol.fitness())
            if self.__interupted == True:
                break
            if i%10 == 0 and not self.__testing:
                progress_callback.emit((bestSol,i))

        return (bestSol,i+2,bestFitnesses,bestForEachIter)
    def __performACOIteration(self):
        antSet=[Ant(self.__matrixSize) for i in range(self.__numberOfAnts)]
        

        for i in range(2*self.__matrixSize*(self.__matrixSize-1)):
            for x in antSet:
                x.addMove(self.__q0,self.__trace,self.__alpha,self.__beta)
        
        for ant in antSet:
            if ant.fitness() == 0:
                return ant
        
            #print(x.fitness())
            #print(trace)
        dTrace=[ 1.0 / antSet[i].fitness() for i in range(len(antSet))]
        for k in range(len(self.__trace)):
            for i in range(len(self.__trace[k])):
                for j in range(len(self.__trace[i])):
                    self.__trace[k][i][j] = (1-self.__rho)*self.__trace[k][i][j]
        for k in range(len(antSet)):
            for i in range(len(antSet[k].getPath())):
                for j in range(len(antSet[k].getPath()[i])-1):
                    x = antSet[k].getPath()[i][j]
                    y = antSet[k].getPath()[i][j+1]
                    self.__trace[i][x][y] += dTrace[k]
        
        bestLocalSolution=[ [antSet[i].fitness(), i] for i in range(len(antSet))]
        bestLocalSolution=max(bestLocalSolution)
        return antSet[bestLocalSolution[1]]
