# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 18:44:00 2020

@author: tamas
"""
import numpy,math 
import copy 
import operator
class InvalidBoardException(Exception):
    pass

def tryEnterForms(gameGrid,forms,rows,columns):
    
    for idx in range(5):
        for i in range(len(forms[idx])):
            for j in range(len(forms[idx][i])):
                if forms[idx][i][j] == '*':
                    if i+rows[idx] < 5 and j+columns[idx] < 6 and gameGrid[i+rows[idx]][j+columns[idx]] == None:
                        gameGrid[i+rows[idx]][j+columns[idx]] = '*'
                        #print("added",i,j,i+rows[idx],j+columns[idx])
                    else:
                        return False
                        #print("fail",i,j,i+rows[idx],j+columns[idx])
            '''for row in forms[idx]:
                print(row)
            print()
            for row in gameGrid:
                print(row)
            print()
            input()'''
    return True
                    
def trySolveRandomGeometricForms(maxTries):
    
    form1 = [['*','*','*','*'],
             [None,None,None,None]]
    
    form2 = [['*',None,'*',None],
             ['*','*','*',None]]
    
    form3 = [['*',None,None,None],
             ['*','*','*',None]]
    
    form4 = [['*','*','*',None],   
             [None,None,'*',None]]

    form5 = [[None,'*',None,None],
             ['*','*','*',None]]

    gameGrid = [[None for i in range(6)] for j in range(5)]
    forms = [form1,form2,form3,form4,form5]
    numberOfTries = 0;
    success = False
    lastTry = None
    Rows = None
    Columns = None
    while numberOfTries < maxTries and not success:
        
        Rows = numpy.random.randint(0,5,5)
        Columns = numpy.random.randint(0,6,5)
        #print(Rows)
        #print(Columns)
        copyGrid = copy.deepcopy(gameGrid)
        success = tryEnterForms(copyGrid,forms,Rows,Columns)
        lastTry = copyGrid
        numberOfTries += 1
        
    if success:
        print("Success " + str(numberOfTries))
    else:
        print("Failure")
        print("Printing last trial")
    for i in range(5):
        print("Form" + str(i) + ": ("+str(Rows[i])+","+str(Columns[i])+")")
    for row in lastTry:
        print(row)
            

def calculateValue(charsToConvert,letterDictionary):
    result = 0
    SIXTEEN = 16
    pos = 0
    for i in range(len(charsToConvert)-1,-1,-1):
        result += letterDictionary[charsToConvert[i]] * SIXTEEN**pos
        pos+=1
    return result
def trySolveRandomCryptoarithmeticGame(maxTries):
    operators={"+" : operator.add, "-": operator.sub, "/": operator.floordiv, "*":operator.mul, "%":operator.mod}
    file = open("cryptarithm.txt")
    letterDictionary = {}
    words = []
    for word in file.read().split():
        words.append(word)
    
    s  = " "
    print(s.join(words))
    currentTry = 0
    success = False
    while currentTry < maxTries and not success:

        for i in range(len(words)):#assign values to the letters
            if words[i] != "=" and words[i] not in operators :
                if len(words[i])==1:
                    letterDictionary[words[i][0]] = numpy.random.randint(0,16)
                    continue
                #res = [] 
                #res[:0] = words[i]
                letterDictionary[words[i][0]] = numpy.random.randint(1,16)
                for j in range(1,len(words[i])):
                    if words[i][j] not in letterDictionary:
                        letterDictionary[words[i][j]] = numpy.random.randint(0,16)
        
        number = calculateValue(words[0],letterDictionary)
        calResult = calculateValue(words[-1], letterDictionary)
        
        i = 1
        while words[i] != "=" and i < len(words):#calculate result
            number = operators[words[i]](number,calculateValue(words[i+1], letterDictionary))
            i += 2
        if calResult == number:
            success = True
        currentTry += 1
        
    if success:
        print("Success")
        print("Success steps taken:" + str(currentTry))
    else:
        print("Failure")
        print("Last try which failed")

    for word in words:
        for char in word:
            if char in letterDictionary:
                print(hex(letterDictionary[char]).split('x')[-1],end="")
            else:
                print(" " + char + " ", end="")
    print()
    
def tryEnterNewNumberSudoku(position,Board):
    boardSize = len(Board)
    lengthProperSquare = int(math.sqrt(boardSize))

    properSquareRow = (position[0]//lengthProperSquare)*lengthProperSquare
    properSquareColumn = (position[1]//lengthProperSquare)*lengthProperSquare
    
    available = list(range(1,boardSize+1))
    

    for i in range(boardSize):#Checking the row
        if Board[i][position[1]] in available:
            available.remove(Board[i][position[1]])

    for j in range(boardSize):#Checking the column
        if Board[position[0]][j] in available:
            available.remove(Board[position[0]][j])

    for i in range(lengthProperSquare):
        for j in range(lengthProperSquare):
            #print(properSquareRow+i,properSquareColumn+j)
            if Board[properSquareRow+i][properSquareColumn+j] in available:
                available.remove(Board[properSquareRow+i][properSquareColumn+j])
                
    if len(available) == 1:
        Board[position[0]][position[1]] = available[0]

        return 1
    elif len(available) != 0:
        chosenvalue = int(numpy.random.randint(0,len(available)))
        Board[position[0]][position[1]] = chosenvalue
        return 1
    if len(available) == 0:
        raise InvalidBoardException("Invalid board!")
    return 0


def solveBoard(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 0:
                board[i][j] = numpy.random.randint(1,len(board))

def verifyBoardCorrectness(board):
    for row in board:
        if len(row) != len(board):
            raise InvalidBoardException("Invalid board!")


def verifyBoardResult(board):
    result = True
    for row in board:
        if numpy.unique(row).size != len(row):
            result = False
    
    if result == False:
        return False
    
    for row in board.transpose():
        if numpy.unique(row).size != len(row):
            result = False

    if result == False:
        return False

    smallSquareLength = int(math.sqrt(len(board)))
    i,j=0,0
    
    while i < len(board) and result:
        while j < len(board[i]) and result:
            
            elems=[]
            
            for k in range(smallSquareLength):
                for kk in range(smallSquareLength):
                    elems.append(board[i+k][j+kk])
                    
            if numpy.unique(elems).size != len(board):
                result = False

            j+=smallSquareLength
        i+=smallSquareLength
        
    return result
def readBoard():
    return numpy.loadtxt("sudoku.txt", "i")

def trySolveRandomSudoku(maxTries):
    gameBoard = readBoard()
    verifyBoardCorrectness(gameBoard)
    
    currentTry = 0
    success = False
    copyBoard = None
    print(gameBoard)
    while currentTry < maxTries and not success:
        
        copyBoard = copy.deepcopy(gameBoard)
        solveBoard(copyBoard)
        success = verifyBoardResult(copyBoard)
        currentTry+=1
    
    if success:
        print("Success steps taken:" + str(currentTry))
        print(copyBoard)
    else:
        print("Fail")
        print("Last try which failed")
        print(copyBoard)

        
def getEmptyPositions(gameBoard,emptyVal):
    listOfEmptyPositions = []
    for i in range(len(gameBoard)):
        for j in range(len(gameBoard[i])):
            if gameBoard[i][j] == emptyVal:
                listOfEmptyPositions.append((i,j))
    return listOfEmptyPositions
def main():
    

    while True:
        
        print('''
    Choose a game:
    1 - Sudoku
    2 - Cryptarithmetic game
    3 - Geometric forms
    0 - exit
              ''')
        try:
            inputAnswer = int(input())
            if inputAnswer == 0:
                return
            print("Number of tries for the computer to make for solution:")
            inputNumberOfTries = int(input())
        
            if inputNumberOfTries <= 0:
                print("Number of tries must be positive!")
            if inputAnswer == 1:
                trySolveRandomSudoku(inputNumberOfTries)
            elif inputAnswer == 2:
                trySolveRandomCryptoarithmeticGame(inputNumberOfTries)
            elif inputAnswer == 3:
                trySolveRandomGeometricForms(inputNumberOfTries)
        except InvalidBoardException as ex:
            print(ex)
        except ValueError as ex:
            print(ex)

    
    
    
    
main()