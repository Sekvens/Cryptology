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
    @return: 
    """
    N = math.ceil(len(cipherText) / mPrime)
    #subCipherList = [cipherText[i:i+N] for i in range(0, len(cipherText),N)] #x^
    subCipherList = []
    for i in range(mPrime): #Create a list with N empty strings
        subCipherList.append("")
    index = 0
    for char in cipherText:
        subCipherList[index % mPrime] += char
        index += 1
    subSum = []
    for subString in subCipherList:
        cipherFTable = frequencyCounter(subString, []) #list[char_i][f_i(x^j)]
        counter = 0 #Avoids a python error
        avgSum = 0
        for i in cipherFTable:
            #Occurence of character i
            fxj = cipherFTable[counter][1]
            #Replace occurence with ic(char_i)
            #cipherFTable[i][1] = (fxj*(fxj-1))/(N*(N-1))
            #sum += (fxj*(fxj-1))/(len(subString)*(len(subString)-1))
            avgSum += (fxj*(fxj-1))
            counter += 1
        subSum.append(avgSum * (1/((len(subString)*(len(subString)-1)))))
    returnSum = 0
    for term in subSum:
        returnSum += term
    return returnSum / mPrime
    
def debugTest(start, stop, fileName):
    cipherText = textoperations.getFileAsString(fileName)
    answers = []
    for i in range(start, stop):
        print(i)
        answers.append([i, 0])
    for i in range(start, stop):
        print("IC for cipherText with mPrime: " + str(i))
        answers[i-start][1] = getIndexOfCoincidence(cipherText, i)
        print(i-start)
    return answers
    
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
    
#Can be used to calculate IC for a language
def pTwoRandom(pList):
    sum = 0
    for probability in pList:
        sum += (probability * probability)
    return sum
    
#Helper for debug, should give the IC for swedish.
def getSweProb():
    pList = []
    for element in debugGetAlphIC():
        pList.append(element[1])
    return pTwoRandom(pList)
    
#Lowest probability for the alphabet. Complete randomness. The proabilty of a coincidence for a uniform random selection from the alphabet.
def getAlphabetRandom(alph):
    n = len(alph)
    sum = 0
    for i in range(n):
        sum = sum + (1/n)*(1/n)
    return sum

#Lowest probability, totally uniform for our language.
def getSweRandom():
    return getAlphabetRandom(textoperations.getAlphabet())
    
def friedmanTest(encryptedText):
    alphabetLength = len(textoperations.getAlphabet())