# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 20:19:24 2020

@author: tamas
"""

import random, copy
from domain import InvalidInputDataException, Node
import numpy as np
class Controller():
    
    
    def __init__(self,repository):
        self.__repository = repository
        self.__evaluator = None
    def pprint_tree(self,node, file=None, _prefix="", _last=True):
        print(_prefix, "`- " if _last else "|- ", node.getLabel(), sep="", file=file)
        _prefix += "   " if _last else "|  "
        child_count = len(node.getChildren())
        for i, child in enumerate(node.getChildren()):
            _last = i == (child_count - 1)
            self.pprint_tree(node.getChildren()[child], file, _prefix, _last)


    def __partitionTheDataWithK(self,valueOfK,testBlockIndex,data):
        
        trainData = []
        testData = []
        for i in range(valueOfK):
            currentSegment = data[ int((i/valueOfK)*len(data)) : int(((i+1)/valueOfK)*len(data)) ]
            if i == testBlockIndex:
                #print(int((i/valueOfK)*len(data)),int(((i+1)/valueOfK)*len(data)))
                testData = currentSegment
            else:
                trainData  = trainData + currentSegment
        
        return trainData,testData
    '''
    def __partitionTheDataRatio(self,ratio,data):
        
        random.shuffle(data)
        dataClassesSet = set([ data[i].getClass() for i in range(len(data))])
        result = []
        for elem in dataClassesSet:
            currentClassEntries = []
            for entry in data:
                if elem == entry.getClass():
                    currentClassEntries.append(entry)
            indexToSplitBy = int(round(ratio*len(currentClassEntries)))
            shuffled = copy.deepcopy(currentClassEntries)
            random.shuffle(shuffled)
            result.append((shuffled[indexToSplitBy:], shuffled[:indexToSplitBy]))
        trainingData = []
        testData = []
        for sublist in result:
            trainingData = trainingData + sublist[0]
            #trainingData = trainingData + sublist[1]
            testData = testData + sublist[1]
        copyTraining = copy.deepcopy(trainingData)
        copyTest = copy.deepcopy(testData)
        random.shuffle(copyTraining)
        random.shuffle(copyTest)

        return copyTraining,copyTest
    
        indexToSplitBy = int(round(ratio*len(data)))
        shuffled = copy.deepcopy(data)
        random.shuffle(shuffled)
        return shuffled[indexToSplitBy:], shuffled[:indexToSplitBy]
    '''
    def __checkIfAllSameClass(self,Data):
        
        dataClassesSet = set([ Data[i].getClass() for i in range(len(Data))])
        if(len(dataClassesSet) == 1):
            return True, Data[0].getClass()
        return False, None

    def __mostFrequentAttribute(self,DataToCheck): 
        DataOfAttributes = [ DataToCheck[i].getClass() for i in range(len(DataToCheck))]
        dictionaryOfAttributes = {} 
        count, itm = 0, '' 
        for item in reversed(DataOfAttributes): 
            dictionaryOfAttributes[item] = dictionaryOfAttributes.get(item, 0) + 1
            if dictionaryOfAttributes[item] >= count : 
                count, itm = dictionaryOfAttributes[item], item 
        return(itm) 


    def __entropy(self,Data):
        resultClasses = {}
        for entry in Data:
            if entry.getClass() not in resultClasses:
                resultClasses[entry.getClass()] = 1
            else:
                resultClasses[entry.getClass()] = resultClasses[entry.getClass()] + 1
        result = 0
        for theClass in resultClasses.keys():
            result += -( (resultClasses[theClass]/len(Data))*np.log2((resultClasses[theClass]/len(Data))))
        return result
            
    
    def __selectAttributeGiniIndex(self,Data,Attributes):
        giniResult = []
        for attrib in Attributes:
            gini = 0
            for value in range(1,5):
                dataForAttirbuteValue = self.__getElementsByAttributeFromData(Data,attrib,value)
                valx = (len(dataForAttirbuteValue)/len(Data))
                valx = value**2
                gini += valx
            giniResult.append([attrib,(1-gini)])
        finalResult = min(giniResult,key=lambda x:x[1])
        return finalResult[0]

    def __selectAttributeInformationGain(self,Data,Attributes):
        allDataEntropy = self.__entropy(Data)
        entropyResult = []
        
        for attrib in Attributes:
            currentEntropy = 0
            for value in range(1,5):
                dataForAttirbuteValue = self.__getElementsByAttributeFromData(Data,attrib,value)
                entropyForAttributeValue = self.__entropy(dataForAttirbuteValue)
                currentEntropy += (len(dataForAttirbuteValue)/len(Data))*entropyForAttributeValue
            gainAttribute = allDataEntropy - currentEntropy
            entropyResult.append([attrib,gainAttribute])
        finalResult = max(entropyResult,key=lambda x:x[1])
        return finalResult[0]
    def __getElementsByAttributeFromData(self,Data,separationAttribute,value):
        result = []
        for entry in Data:
            if entry.getAttributes()[separationAttribute] == value:
                result.append(entry)
        return result
    def __generateTree(self,Data,Attributes):
        newNode = Node()
        result,theClass = self.__checkIfAllSameClass(Data)
        if result == True:
            #print("All same")
            newNode.setIsLeaf(True)
            newNode.setLabel(theClass)
            return newNode
        else:
            if len(Attributes) == 0:
                #print("No attributes")
                newNode.setIsLeaf(True)
                newNode.setLabel(self.__mostFrequentAttribute(Data))
                return newNode
            else:
                separationAttribute = self.__evaluator(Data,Attributes)
                newNode.setLabel(separationAttribute)
                for value in range(1,6):#This should be more generic, but now it's "OK" all possible values of separation value
                    partialData = self.__getElementsByAttributeFromData(Data,separationAttribute,value)
                    if len(partialData) == 0:
                        newLabel = self.__mostFrequentAttribute(Data)
                       # print("Most frequent" + str(newLabel))
                        newLeaf = Node(label=newLabel,isLeaf=True)
                        newNode.addChild(value,newLeaf)
                    else:
                       # print("Recursive call" + str(value))
                        newAttributes = copy.deepcopy(Attributes)
                        newAttributes.remove(separationAttribute)
                        newChild =self.__generateTree(partialData,newAttributes)
                        newNode.addChild(value, newChild)
                return newNode

    def __testTree(self,root,testData):
        correct = 0
        for entry in testData:
            current = root
            while not current.isLeaf():
                current = current.getChildren()[entry.getAttributes()[current.getLabel()]]
            if current.getLabel() == entry.getClass():
                correct+=1
        return (correct/len(testData))*100
    
    def evaluateWithGiniIndex(self,valueOfK=5):
        initialData = self.__repository.getAllData()
        random.shuffle(initialData)
        self.__evaluator = self.__selectAttributeGiniIndex
        accuracyResults = []

        for i in range(valueOfK):
            trainingData,testData = self.__partitionTheDataWithK(valueOfK,i,initialData)
            #print(len(trainingData),len(testData))
            if(len(trainingData) == 0 or len(testData)==0 ):
                raise InvalidInputDataException("Invalid initialization, empty dataset")
            root = self.__generateTree(trainingData,list(trainingData[0].getAttributes().keys()))
            accuracyResults.append(self.__testTree(root,testData))
        
        #print(accuracyResults)
        return sum(accuracyResults)/len(accuracyResults)

    def evaluateWithInformationGain(self,valueOfK=5):
        initialData = self.__repository.getAllData()
        random.shuffle(initialData)
        self.__evaluator = self.__selectAttributeInformationGain
        accuracyResults = []
        for i in range(valueOfK):
            trainingData,testData = self.__partitionTheDataWithK(valueOfK,i,initialData)
            #print(len(trainingData),len(testData))
            if(len(trainingData) == 0 or len(testData)==0 ):
                raise InvalidInputDataException("Invalid initialization, empty dataset")
            root = self.__generateTree(trainingData,list(trainingData[0].getAttributes().keys()))
            accuracyResults.append(self.__testTree(root,testData))
        
        #print(accuracyResults)
        return sum(accuracyResults)/len(accuracyResults)
        
    def runTests(self,dataRatio=0.3):
        IGTests = []
        GINITests = []
        for i in range(1000):
            print("Test number: " + str(i+1) + " finished")
            IGTests.append(self.evaluateWithInformationGain(dataRatio))
            GINITests.append(self.evaluateWithGiniIndex(dataRatio))
        
        avgIG = sum(IGTests)/len(IGTests)
        avgGini = sum(GINITests)/len(GINITests)
        return (avgIG,avgGini,IGTests,GINITests)