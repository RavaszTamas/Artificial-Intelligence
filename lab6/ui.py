# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 13:36:55 2020

@author: tamas
"""


from domain import InvalidInputDataException
import matplotlib.pyplot as plt

class Console():
    
    
    def __init__(self,controller):
        self.__controller = controller
    def __printMenu(self):
        s = ""
        #s +="Default ratio between training data and test data is 0.3 ( from a 100 70 is for training 30 is for test)\n"
        s +="Default value for k is 10, for cross validation step\n"
        s += "1. Construct tree with information gain.\n"
        s += "2. Construct tree with gini index.\n"
        s += "3. Tests.\n"
        s += "0. Exit.\n"
        print(s)
    '''
    def readInputData(self):
        ratio = 0.3
        try:
            print("Input the percentage for hold out tesint (implicit n=0.3)")
            ratio = float(input("ratio = "))
            if ratio <= 0 or ratio >= 1.0:
                raise Exception
        except :
            print("invalid number, the implicit value is still 0.3")
            ratio=0.3
        return ratio
    '''
    def readInputDataInteger(self):
        ratio = 10
        try:
            print("Input the size of a validation parition (implicit n=10) needs to be at least 2")
            ratio = int(input("ratio = "))
            if ratio <= 1:
                raise Exception
        except :
            print("invalid number, the implicit value is still 10")
            ratio=10
        return ratio

    def __executeConstructTreeInfoGain(self):
        ratio = self.readInputDataInteger()
        result = self.__controller.evaluateWithInformationGain(ratio)
        print("Percentage of correctness = " +str(result) + "%")

    def __executeConstructTreeGini(self):
        ratio = self.readInputDataInteger()
        result = self.__controller.evaluateWithGiniIndex(ratio)
        print("Percentage of correctness = " +str(result) + "%")

    def __runTests(self):
        valueOfK = self.readInputDataInteger()
        result = self.__controller.runTests(valueOfK)
        print("Percentage of correctness information gain= " +str(result[0]) + "%")
        print("Percentage of correctness gini index= " +str(result[1]) + "%")
        plt.plot(result[2], label="Information gain")
        plt.plot(result[3], label="Gini index")
        plt.legend()
        plt.title('The best fitness average for each iteration')
        plt.savefig('test_fresh.png')
        plt.show()
        
        text_file = open("test_result.txt", "w")
        text_file.write("Percentage of correctness information gain= " +str(result[0]) + "%"+"\n"+"Percentage of correctness gini index= " +str(result[1]) + "%" + 
                            "\nValue of k = " + str(valueOfK))
        text_file.close()


    def run(self):
        while True:
            try:
                self.__printMenu()
                inputCommand = input().strip()
                if inputCommand== "1":
                    self.__executeConstructTreeInfoGain()
                elif inputCommand== "2":
                    self.__executeConstructTreeGini()
                elif inputCommand== "3":
                    self.__runTests()
                elif inputCommand== "0":
                    return
            except InvalidInputDataException as ex:
                print(str(ex) + "\nTry a different ratio")