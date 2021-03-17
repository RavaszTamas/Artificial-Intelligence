
import numpy as np
import json
from copy import deepcopy
import matplotlib as mpl

class UnableToObtainResultException(Exception):
    pass

def membershipFunctionFactoryCut(a,b,c,d,cut):
    if not( a <= b and b <= c and c <= d):
        raise Exception("Invalid input for membership function")
    if a == b and b == c and c == d:
        return lambda x: a
    if a == b and c == d:
        return lambda x: cut
    if a == b:
        return lambda x:max(0,min(cut,(d-x)/(d-c)))
    if c == d:
        return lambda x: max(0,min((x-a)/(b-a),cut))

    return lambda x: max(0,min((x-a)/(b-a),cut,(d-x)/(d-c)))


def membershipFunctionFactory(a,b,c,d):
    if not( a <= b and b <= c and c <= d):
        raise Exception("Invalid input for membership function")
    if a == b and b == c and c == d:
        return lambda x: a
    if a == b and c == d:
        return lambda x: 1
    if a == b:
        return lambda x:max(0,min(1,(d-x)/(d-c)))
    if c == d:
        return lambda x: max(0,min((x-a)/(b-a),1))

    return lambda x: max(0,min((x-a)/(b-a),1,(d-x)/(d-c)))


class Definition():
    '''
    Representation of a fuzzy variable, it contains the functions representing a 
    fuzzy region
    '''
    def __init__(self):
        self.functions = {}
        self.inverse = {}

    
    def addFunction(self,variableName,membershipFunction,inverse=None):
        '''
        Adds a function that belongs to a fuzzy set
        Represents a region for a given variable
        Invertable is used for the output functions
        '''
        
        self.functions[variableName] = membershipFunction
        self.inverse[variableName] = inverse
        
        
    def fuzzifyInput(self,inputValue):
        '''
        Fuzzifies the given input data based on the membership functions
        '''
        result = {}
        for nameOfRegion, membershipFunction in self.functions.items():
            result[nameOfRegion] = membershipFunction(inputValue)
        return result
    
    
    def calculateInverse(self,mameOfVariable,obtainedValue):
        
        self.inverse[mameOfVariable](obtainedValue)

class Rule():
        def __init__(self, inputData, outputName):
            """
                Receives the set of inputs and expected output
            """
            self.inputData = inputData
            self.outputVariableName = outputName  # the name of the output variable

        def evaluate(self, inputData):
            """
                Receives a dictionary of all the input values and returns the conjunction
                of their values
            """
            result=[self.outputVariableName]
            listOfAllValues = []
            for definitionName,variableName in self.inputData.items():
                listOfAllValues.append(inputData[definitionName][variableName])
            union = min(listOfAllValues)
            result.append(union)
            return result

class FuzzySystem():
    """
        Given the definitions of the inputs and outputs,
        and the decision "matrix" it will compute the the result of the 
        fuzzy system
    """

    def __init__(self, filename="problem.in"):
        self.__filname = filename
        self.inputDefinitions = {}
        self.outputDefinition = None
        self.aggregatedOutputDefinition = None
        self.fuzzyRules = []
        self.outputFunctionParameters = {}
        self.outputName = None
        self.valueRange = None
        self.__initializeSystem()
    def __initializeSystem(self):
        problemDescription = open(self.__filname, 'r')
        jsonList = json.loads(problemDescription.read())
        dataCharts = jsonList['problem_details'][0]['definition_charts']
        for item in dataCharts:
            nameOfDefinition = item['name']
            newDefinition = Definition()
            valuesOfChart = item['values']
            #print(nameOfChart,valuesOfChart)
            for valueItem in valuesOfChart:
                nameOfFunction = valueItem['name']
                paramsOfFunction = valueItem['region']
                #print(nameOfFunction,paramsOfFunction)
                newDefinition.addFunction(nameOfFunction,membershipFunctionFactory(*paramsOfFunction))
            self.addDefinition(nameOfDefinition,newDefinition)

        outputData = jsonList['problem_details'][0]['output']
        
        nameOfDefinition = outputData['name']
        self.outputName = nameOfDefinition
        outputDefinition = Definition()
        valuesOfChart = outputData['values']
        #print(nameOfChart,valuesOfChart)
        for valueItem in valuesOfChart:
            nameOfFunction = valueItem['name']
            paramsOfFunction = valueItem['region']
            #print(nameOfFunction,paramsOfFunction)
            self.outputFunctionParameters[nameOfFunction]=paramsOfFunction
            outputDefinition.addFunction(nameOfFunction,membershipFunctionFactory(*paramsOfFunction))

        self.setOutputDefinition(outputDefinition)

        ruleMatrix = jsonList['problem_details'][1]['rules']

        for item in ruleMatrix:
            premise = item['premise']
            conclusion = item['conclusion']
            premiseDictionary = {}
            for premiseElem in premise:
                premiseDictionary[premiseElem['name']] = premiseElem['value']
            
            conclusionDictionary = {}
            conclusionDictionary[conclusion['name']] = conclusion['value']
            self.addRule(Rule(premiseDictionary,conclusionDictionary))
            
        rangeOfValues = jsonList['problem_details'][2]['range']
        self.valueRange = (rangeOfValues["start"],rangeOfValues["end"])
        problemDescription.close()
    def addDefinition(self, name, definition):
        """
        Receives a definition, with the name and the corresponding data
        """
        self.inputDefinitions[name] = definition
    
    def addRule(self,rule):
        self.fuzzyRules.append(rule)
    
    def setOutputDefinition(self, definition):
        """
        Receives the output for the system, with the name and the corresponding data
        """
        self.outputDefinition = definition


    def evaluateInput(self,inputData):
        #print(inputData)
        fuzzyValues = self.__computeFuzzyValuesForInput(inputData)
        #print(fuzzyValues)
        ruleValues = self.__computeRuleValuesForFuzzyData(fuzzyValues)
        ruleValues = sorted(ruleValues,key=lambda x: x[1],reverse=True)
        #print(ruleValues)
        self.__constructAggeragatedFunctions(ruleValues)
 
        if len(ruleValues) == 0:
            raise UnableToObtainResultException("Based on the input data all fuzzy results have obtained a 0 value. No result can be obtained")
        
        result = [max(val for name, val in self.aggregatedOutputDefinition.fuzzifyInput(i).items()) for i in range(self.valueRange[0],self.valueRange[1]+1)]       
        #yresult = [max(val for name, val in self.outputDefinition.fuzzifyInput(i).items()) for i in range(self.valueRange[0],self.valueRange[1]+1)]       
        xValues = [i for i in range(self.valueRange[0],self.valueRange[1]+1)]
        
        '''
        s = ""
        for elem in list(zip(result,xValues)):
            s += str(elem[0]) + " * " +str(elem[1]) + " + "
        print(s)
        s = ""
        for elem in result:
            s += str(elem) + " + "
        print(s)
        '''
        #mpl.pyplot.plot(xValues, result, label='loss value vs iteration')
        #mpl.pyplot.plot(xValues, yresult, label='loss value vs iteration')

        #mpl.pyplot.show()

        
        return self.__calculateCenterOfGravityArea(xValues,result)

    def __calculateCenterOfGravityArea(self,xValues,yValues):
        
        weightedTotal = 0
        weightSum = sum(yValues)

        for i in range(len(yValues)):
            weightedTotal += yValues[i]*xValues[i]
            
        return weightedTotal/weightSum
        
    def __constructAggeragatedFunctions(self,ruleValues):
        #print(self.outputFunctionParameters)
        alreadyAdded = []
        newAggregatedDefinition = Definition()
        for elem in ruleValues:
            if elem[0][self.outputName] not in alreadyAdded:
                
                alreadyAdded.append(elem[0][self.outputName])
                params=deepcopy(self.outputFunctionParameters[alreadyAdded[-1]])
                params.append(elem[1])
                #print(alreadyAdded[-1],params)
                newAggregatedDefinition.addFunction(alreadyAdded[-1],membershipFunctionFactoryCut(*params))
        self.aggregatedOutputDefinition = newAggregatedDefinition
    def __computeRuleValuesForFuzzyData(self,fuzzyValues):
        returnList=[]
        for rule in self.fuzzyRules:
            resultOfComputation = rule.evaluate(fuzzyValues)
            #if resultOfComputation[1] != 0:
            returnList.append(resultOfComputation)
        
        return returnList
    def __computeFuzzyValuesForInput(self, inputData):
        
        returnDictionary = {}
        for variableName, value in inputData.items():
            returnDictionary[variableName] = self.inputDefinitions[variableName].fuzzifyInput(inputData[variableName])
        
        return returnDictionary
        