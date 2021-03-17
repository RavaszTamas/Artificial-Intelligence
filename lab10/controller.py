
from model import FuzzySystem,UnableToObtainResultException
import view
import json

class Controller():
    
    def __init__(self,fuzzySystem, filename="input.in"):
        self.__view = view.View(fuzzySystem)
        self.__system = fuzzySystem
        self.__inputs = []
        self.__currentInput = -1
        self.__filename = filename
        self.__readInputs()
        
    
    def __readInputs(self):
        inputProblemData = open(self.__filename, 'r')
        jsonList = json.loads(inputProblemData.read())
        inputs = jsonList["inputs"]
        for inputCandidate in inputs:
            parameters = inputCandidate["parameters"]
            paramDictionary = {}
            for parameter in parameters:
                paramDictionary[parameter["name"]] = parameter["value"]
            self.__inputs.append(paramDictionary)
        
        if len(self.__inputs) != 0:
           self.__currentInput = 0 
    def __computeForNextInput(self):
        
        if self.__currentInput == -1:
            self.__view.printMessage("No inputs are loaded!")
            return
        
        if self.__currentInput == len(self.__inputs):
            self.__currentInput = 0
        try:
            result = self.__system.evaluateInput(self.__inputs[self.__currentInput])
            self.__view.printResult(self.__inputs[self.__currentInput],result)

        except UnableToObtainResultException as ex:
            self.__view.printResult(self.__inputs[self.__currentInput],str(ex))
            
        self.__currentInput +=1

    def start(self):
        
        
        while True:
            self.__view.printMenu()
            command = input("enter the command: ")
            if command == "next":
                self.__computeForNextInput()
            elif command == "read new":
                self.__readInputs()
            elif command == "exit":
                return
            else:
                print("Invalid input")