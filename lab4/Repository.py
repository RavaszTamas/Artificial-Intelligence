# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 13:30:19 2020

@author: tamas
"""

class PopulationRepository():
    
    def __init__(self):
        self.__population = []    
        self.__neighbourHood = {}

    def setPopulation(self,newPopulation):
        self.__population = newPopulation
        
    def setNeighbourHood(self,particle, newNeighbourHood):
        self.__neighbourHood[particle] = newNeighbourHood

    def getNeighbourHood(self,particle):
        return self.__neighbourHood[particle]


    def getPopulation(self):
        return self.__population
        
    def __len__(self):
        return len(self.__population)