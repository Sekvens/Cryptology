import textoperations
import os
import math

alphabet = textoperations.getAlphabet()

#Will return a list list in the style [[a, 0], [b, 0], ...
def getEmptyFrequencySet():
    tempList = []
    for char in alphabet:
        element = [char, 0]
        tempList.append(element)
    return tempList

def frequencyCounter(inputText, frequencyTable):
    """Count frequency occurence of characters in the alphabet and adds it to the provided table. If it's empty list then it creates a new empty table. 
    This function is not safe! The string have to follow the standard of the lab."""
    if(len(frequencyTable)==0):
        frequencyTable = getEmptyFrequencySet()
    for char in inputText:
        charNr = alphabet.find(char)
        frequencyTable[charNr][1] += 1
    return frequencyTable
    
#Transforms the values into percentage!
def transformFTable(frequencyTable):
    sum = 0
    for charContrainer in frequencyTable:
        sum = sum + charContrainer[1]
    for charContrainer in frequencyTable:
        charContrainer[1] = round((charContrainer[1]*100 / sum), 3)
    return frequencyTable
    
def getFrequencyFromFile(fileName, frequencyTable):
    inputString = textoperations.getFormattedStringFromFile(fileName)
    print("Working with file: \n" + fileName + " File length: " + str(len(inputString)))
    tempTable = frequencyCounter(inputString, frequencyTable)
    return tempTable
    
def getFrequencyFromFolder(folderPath, frequencyTable):
    ftable = frequencyTable
    fCounter = 0
    for fileName in os.listdir(folderPath):
        ftable = getFrequencyFromFile(folderPath + os.sep + fileName, ftable)
        fCounter += 1
    print("Collected Frequency from " + str(fCounter) + " files")
    return ftable
    
#Helper for debug
def getCurrentPath():
    return os.path.dirname(os.path.realpath(__file__))
    
def getIndexOfCoincidence(cipherText, mPrime):
    """
    This calculates K_o or what's called IC(x^j). 
    @return: A fTable.
    """
    N = math.ceil(len(cipherText) / mPrime)
    subCipherList = [cipherText[i:i+N] for i in range(0, len(cipherText),N)]
    totalSum = []
    for subString in subCipherList:
        cipherFTable = frequencyCounter(subString, [])
        counter = 0
        sum = 0
        for i in cipherFTable:
            #Occurence of character i
            fxj = cipherFTable[counter][1]
            #Replace occurence with ic(char_i)
            #cipherFTable[i][1] = (fxj*(fxj-1))/(N*(N-1))
            sum += (fxj*(fxj-1))/(N*(N-1))
            counter += 1
        totalSum.append(sum)
    returnSum = 0
    for subSum in totalSum:
        returnSum += subSum
    return returnSum / mPrime
    
def debugTest(nr):
    cipherText = textoperations.getFileAsString("test.txt")
    for i in range(nr):
        print("IC for cipherText with mPrime:" + str(i+1))
        print(getIndexOfCoincidence(cipherText, i+1))
    
def getICTableAlphabet(fileName):
    """Reads a file where every row have the letter and occurence as a percentage seperated by |"""
    alphF = textoperations.getFileAsString(fileName).split('\n')
    i = 0
    for dataString in alphF:
        dataString = dataString.split('|')
        f = 0.0
        f = float(dataString[1])
        alphF[i] = [dataString[0], f]
        i += 1
    return alphF
    
def debugGetAlphIC():
    return getICTableAlphabet("sweletterfrequency.txt")
    
# def getAverageIndexOfCoincidence(icTable, mPrime):#mPrime):
    # """This is the likleyhood that two random elements are identical. It's an average of all index of coincidence for a string."""
    # sum = 0
    # for tuple in icTable: #mPrime?
        # sum += tuple[1]
    # return ((1/len(icTable)) * sum)
    
#Can be used to calculate IC for a language
def pTwoRandom(pList):
    sum = 0
    for probability in pList:
        sum += (probability * probability)
    return sum
    
#Lowest probability for the alphabet. Complete randomness. The proabilty of a coincidence for a uniform random selection from the alphabet.
def getAlphabetRandom(alph):
    n = len(alph)
    sum = 0
    for i in range(n):
        sum = sum + (1/n)*(1/n)
    return sum
    
def getLanguageFrequency():
    print("todo later")
    
def friedmanTest(encryptedText):
    alphabetLength = len(textoperations.getAlphabet())
    probability_char