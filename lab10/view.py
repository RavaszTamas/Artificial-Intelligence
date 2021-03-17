

class View():
    
    def __init__(self,fuzzySystem,filename="output.out"):
        self.__fuzzySystem = fuzzySystem
        self.__filename = filename
    
    def showLastResult(self):
        pass
    
    def printMessage(self,message):
        print(message)
        
    def printMenu(self):
        s = "\n"
        s += "next - in order to print the result of the next input\n"
        s += "read new - read a new set of inputs\n"
        s += "exit - exit the application\n"
        s += "\n"
        print(s)
        
    def printResult(self,inputData,result):
        s = "For the give input data:\n"
        for name,value in inputData.items():
            s += str(name) + " with value: "  + str(value) + "\n"
        s +="the suggested operating time is: "+str(result)
        print(s)
        outputFile = open(self.__filename, 'a+')
        s+="\n\n"
        outputFile.write(s)
    
        outputFile.close()
