# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 18:27:35 2020

@author: tamas
"""
from time import time


class Configuration():
    def __init__(self, positions):
        self.__values = positions[:]

    def getSize(self):
        return len(self.__values)

    def getValues(self):
        return self.__values[:]

    def validPosition(self,j):
        '''
        Checks if a position is valid on the last row of the board
        j = column on the last row of the board
        '''
        i = len(self.__values)

        if j in self.__values:
            return False
    
        for k in range(len(self.__values)):
            if abs(i - k) - abs(j - self.__values[k]) == 0:
                return False

        return True
        
    def nextConfiguration(self,j):
        '''
        Generates the next configuration based on the current one for that column in the
        last row of the board
        j = column on the last row of the board
        '''
        i = len(self.__values)

        if j in self.__values:
            return []
    
        for k in range(len(self.__values)):
            if abs(i - k) - abs(j - self.__values[k]) == 0:
                return []
        
        aux = self.__values[:]
        aux.append(j)
        return [Configuration(aux)]
    
    def __eq__(self, other):
        if not isinstance(other, Configuration):
            return False
        if self.getSize() != other.getSize():
            return False
        for i in range(self.getSize()):
            if self.__values[i] != other.getValues()[i]:
                return False
        return True

    def __str__(self):
        return str(self.__values)
    def __repr__(self):
        return str(self)

class State():
    def __init__(self, finalSize):
        self.__values = []
        self.__finalSize = finalSize
    
    def setValues(self, values):
        self.__values = values[:]

    def getValues(self):
        return self.__values[:]

    def __str__(self):
        s=''
        matr = [[0 for x in range(self.__finalSize)] for y in range(self.__finalSize)]
        #print(self.__values[-1])
        values = self.__values[-1].getValues()
        for i in range(len(values)):
            matr[i][values[i]] = 1
        for line in matr:
            s += str(line) + "\n"
        s += "Chosen columns for each row: \n"
        s += str(values) + "\n"
        return s

    def __add__(self, something):
        aux = State(self.__finalSize)
        if isinstance(something, State):
            aux.setValues(self.__values+something.getValues())
        elif isinstance(something, Configuration):
            aux.setValues(self.__values+[something])
        else:
            aux.setValues(self.__values)
        #print(aux.getValues())
        return aux


class Problem():
    
    def __init__(self, initial,final):
        self.__initialConfig = initial
        self.__initialState = State(final)
        self.__finalValue = final
        self.__initialState.setValues([self.__initialConfig])

    def getRoot(self):
        return self.__initialState

    def isFinalState(self,stateToCheck):
        '''
        Checks if the current state is a final one
        Parameters
        ----------
        stateToCheck : State, the state to be checked

        Returns
        -------
        True if the current stage is a final one, False otherwise

        '''
        if len(stateToCheck.getValues()[-1].getValues()) >= self.__finalValue:
            return True
        return False
    
    def expand(self,stateToExpand):
        myList = []
        currentConfiguration = stateToExpand.getValues()[-1]
        for i in range(self.__finalValue):
            for x in currentConfiguration.nextConfiguration(i):
                myList.append(stateToExpand + x)
                
        return myList

    def heuristics(self, state):
        '''
        Heuristic for the state, the fewer the available positions on the next available row
        the smaller the cost, if no available position, cost is maximal to not to check
        states which can not have a solution

        Parameters
        ----------
        state : State, the for which the heuristics is evaluated

        Returns
        -------
        integer - cost for that state

        '''
        count = self.__finalValue*2
        finalConfiguration = state.getValues()[-1]
        for i in range(self.__finalValue):
            if not finalConfiguration.validPosition(i):
                count = count - 1
        
        if count == self.__finalValue:
            return self.__finalValue*2
        
        return count

    

class Controller():
    
    
    def __init__(self,problem):
        self.__problem = problem
    
    def DFS(self, root,firstOnly):
        st = [root]
        solutions=[]
        while len(st) > 0:
            currentState = st.pop()

            if self.__problem.isFinalState(currentState):
                if firstOnly:
                    return currentState
                solutions.append(currentState)
            else:
                st = st + self.__problem.expand(currentState)
            
            
        return solutions

    def Greedy(self,root):
        visited = []
        toVisit = [root]
        solutions = []
        while len(toVisit) > 0:
            currentState = toVisit.pop(0)
            visited.append(currentState)
            if self.__problem.isFinalState(currentState):
                return currentState
            aux=[]
            for x in self.__problem.expand(currentState):
                if x not in visited:
                    aux.append(x)
                    
            aux = [ [x, self.__problem.heuristics(x)] for x in aux]
            aux.sort(key=lambda x:x[1])
            aux = [x[0] for x in aux]

            toVisit = aux[:] + toVisit 
        return solutions

class UI():
    
    def __init__(self):
        self.__iniC = Configuration([])
        self.__problem = Problem(self.__iniC,4)
        self.__controller = Controller(self.__problem)
    
    def printMenu(self):
        s = ''
        s += "0 - exit \n"
        s += "1 - read the matrix size \n"
        s += "2 - find a path with DFS, print first found \n"
        s += "3 - find a path with DFS, all possible solutions \n"
        s += "4 - find path with greedy method, first found solution \n"
        s += "5 - check until 100 \n"
        print(s)
    
    def readNewConfiguration(self):
        n = 3
        try:
            print("Input the number of rows of the matrix (implicit n=4)")
            n = int(input("n = "))
            if n <= 0:
                raise Exception
        except :
            print("invalid number, the implicit value is still 4")
            n=4
        self.__iniC = Configuration([])
        self.__problem = Problem(self.__iniC,n)
        self.__controller = Controller(self.__problem)
    
    def findPathDFS(self):
        startClock = time()
        print(str(self.__controller.DFS(self.__problem.getRoot(),True)))
        print('execution time = ',time()-startClock, " seconds" )

    
    def findPathDFSAll(self):
        startClock = time()
        count = 0
        for solution in self.__controller.DFS(self.__problem.getRoot(),False):
            print(solution)
            count +=1
        print("Number of solutions: " + str(count))
        print('execution time = ',time()-startClock, " seconds" )

    def findPathGreedy(self):
        startClock = time()
        print(str(self.__controller.Greedy(self.__problem.getRoot())))
        print('execution time = ',time()-startClock, " seconds" )

    def checkForOneHundred(self):
        for n in range(0,101):
            self.__iniC = Configuration([])
            self.__problem = Problem(self.__iniC,n)
            self.__controller = Controller(self.__problem)
            startClock = time()
            self.__controller.Greedy(self.__problem.getRoot())
            f = open("demofile2.txt", "a")
            f.write("n = " + str(n) + ' execution time = ' + str(time()-startClock) + " seconds\n" )
            f.close()


    def run(self):
        mainRun = True
        
        while mainRun:
            self.printMenu()            
            try: 
                choice = int(input(">>>"))
                if choice == 0:
                    return
                elif choice == 1:
                    self.readNewConfiguration()
                elif choice == 2:
                    self.findPathDFS()
                elif choice == 3:
                    self.findPathDFSAll()
                elif choice == 4:
                    self.findPathGreedy()
                elif choice == 5:
                    self.checkForOneHundred()
            except ValueError:
                print('invalid command')

def tests():
    c1 = Configuration([])
    final_value = 4
    s = State(final_value)
    p = Problem(c1,final_value)
    
    #Configuration
    assert(c1.getSize()==0)
    assert(c1.getValues()==[])
    config = c1.nextConfiguration(1)
    assert(config == [Configuration([1])])
    
    config2 = config[-1].nextConfiguration(3)
    assert(config2[0] == Configuration([1,3]))
    
    #State
    
    assert(s.getValues() == [])
    s = s + 'ceva aiurea'
    assert(s.getValues() == [])
    s = s + c1
    assert(s.getValues() == [c1])
    
    #print("dsa")
    #Problem
    aux = p.expand(s)
    #("asd")
    #for elem in aux:
        #print(elem)
    assert(len(aux) == 4)
    assert(aux[1].getValues()[-1] == Configuration([1]))
    
    #...
    
    print('tests passed')
    
def main():
    tests()
    ui = UI()
    ui.run()
    
    
    
main()    
