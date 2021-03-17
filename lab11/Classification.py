# -*- coding: utf-8 -*-
"""
Created on Wed May 27 21:53:24 2020

@author: tamas
"""

from deap import creator,base,tools,algorithms
from sklearn.model_selection import train_test_split
from random import random, shuffle
import numpy as np
import deap.gp as gp
import operator
from math import sin,cos
import csv

def classifisation(value):
    if(value < -1):
        return "Move-Forward"
    if(-1<=value and value < 0):
        return "Slight-Right-Turn"
    if(0<=value and value < 1):
        return "Sharp-Right-Turn"
    return "Slight-Left-Turn"


class GeneticTreeModel():

    
    def __init__(self,inputData,additionalTerminals,maxDepthOfTree=10):
        self.__pop = None
        self.__stats = None
        self.__hof = None
        self.__testResult = None
        pset = gp.PrimitiveSet("main", 24, "IN")
        pset.addPrimitive(max, 2)
        pset.addPrimitive(operator.add, 2)
        pset.addPrimitive(operator.mul, 2)
        pset.addPrimitive(operator.sub, 2)
        pset.addPrimitive(sin, 1)
        pset.addPrimitive(cos, 1)
        '''
        10 random terminals
        '''
        for i in range(10):
            pset.addTerminal(random())
            
        for i in additionalTerminals:
            pset.addTerminal(i)

        '''
        initialData = []
        with open('sensor_readings_24.data', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                initialData.append(row)
        '''
        initialData = np.array(inputData)
        
        shuffle(initialData)
        
        
        X = initialData[:,:-1]
        X = X.astype(float)
        Y = initialData[:,-1]
        
        XTrain, XTest, YTrain, YTest = train_test_split(X,Y,test_size=0.2)

        self.__XTrain =  XTrain
        self.__YTrain = YTrain
        self.__XTest = XTest
        self.__YTest = YTest


        evaluator = lambda x: self.evalRobotDirection(x)

        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMax)
        
        toolbox = base.Toolbox()
        toolbox.register("expr", gp.genGrow, pset=pset, min_=3, max_=maxDepthOfTree)
        toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)
        toolbox.register("compile", gp.compile, pset=pset)
        toolbox.register("evaluate", evaluator)
        toolbox.register("select", tools.selTournament, tournsize=7)
        toolbox.register("mate", gp.cxOnePoint)
        toolbox.register("expr_mut", gp.genGrow, min_=0, max_=2)
        toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)
        
        
        self.__toolbox = toolbox
        
        
    def evaluate(self,iterations,popNum):
            pop = self.__toolbox.population(n=popNum)
            hof = tools.HallOfFame(1)
            stats = tools.Statistics(lambda ind: ind.fitness.values)
            stats.register("avg", np.mean)
            stats.register("std", np.std)
            stats.register("min", np.min)
            stats.register("max", np.max)
            
            algorithms.eaSimple(pop, self.__toolbox, 0.8, 0.1, iterations, stats, halloffame=hof)
            
            func = self.__toolbox.compile(expr=hof[0])
            testRatio = sum(classifisation(func(*in_)) == out for in_, out in zip(self.__XTest,self.__YTest))/len(self.__YTest)

            self.__pop = pop
            self.__hof = hof
            self.__stats = stats
            self.__testResult = testRatio
            
    def obtainLastResult(self):
        if self.__pop == None:
            raise Exception("No result yet")
        return self.__pop,self.__stats,self.__hof,self.__testResult
    def evalRobotDirection(self,individual):
        func = self.__toolbox.compile(expr=individual)
        return sum(classifisation(func(*in_)) == out for in_, out in zip(self.__XTrain,self.__YTrain)),

        
    
    
    
    
    
    
    
