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
    
#Helpfunction for refactorisation.
def getSubCipherList(cipherText, mPrime):
    subCipherList = []
    for i in range(mPrime): #Create a list with N empty strings
        subCipherList.append("")
    index = 0
    for char in cipherText:
        subCipherList[index % mPrime] += char
        index += 1
    return subCipherList
    
def getIndexOfCoincidence(cipherText, mPrime):
    """
    Does not support keys of size less than 3. Return the IC for the key size mPrime Calculates index of coincidence for a key of length mPrime for the given ciphertext.
    @mPrime: Possible key length.
    @cipherText: The encrypted text.
    @return: IC_mprime(cipherText)
    """
    N = math.ceil(len(cipherText) / mPrime)
    #subCipherList = [cipherText[i:i+N] for i in range(0, len(cipherText),N)] #x^
    subCipherList = getSubCipherList(cipherText, mPrime)
    subSum = []
    for subString in subCipherList:
        cipherFTable = frequencyCounter(subString, []) #list[char_i][f_i(x^j)]
        counter = 0 #Avoids a python type error
        avgSum = 0
        for i in cipherFTable:
            #Occurence of character i
            fxj = cipherFTable[counter][1]
            #Replace occurence with ic(char_i)
            avgSum += (fxj*(fxj-1))
            counter += 1
        subSum.append(avgSum * (1/((len(subString)*(len(subString)-1)))))
    returnSum = 0
    for term in subSum:
        returnSum += term
    return returnSum / mPrime        
    
def getICforKeyLengths(start, stop, fileName):
    cipherText = textoperations.getFileAsString(fileName)
    answers = []
    for i in range(start, stop+1):
        answers.append([i, 0])
    for i in range(start, stop+1):
        answers[i-start][1] = getIndexOfCoincidence(cipherText, i)
    maximum = 0.0
    maxKey = 0
    sKey = 0
    sMax = 0.0
    for keyIC in answers:
        if(keyIC[1]>maximum):
            sKey = maxKey
            sMax = maximum
            maximum = keyIC[1]
            maxKey = keyIC[0]
    print("Maximum IC found is: ", maximum, " for key of length ", maxKey)
    print("Second largest pair is (", sKey, ", ", sMax, ")")
    return answers
    
def getPTableAlphabet(fileName):
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
    
def debugGetAlphP():
    return getPTableAlphabet("sweletterfrequency.txt")
    
#Can be used to calculate IC for a language
def pTwoRandom(pList):
    sum = 0
    for probability in pList:
        sum += (probability * probability)
    return sum
    
#Helper for debug, should give the IC for swedish.
def getSweProb():
    pList = []
    for element in debugGetAlphP():
        pList.append(element[1])
    return pTwoRandom(pList)
    
def getChiSquared(nrOfChar, expectedNrOfChar):
    """Get the chi square for one letter"""
    return ((nrOfChar - expectedNrOfChar)(nrOfChar - expectedNrOfChar))/expectedNrOfChar

def getChiSquaredStatistics(charOccurenceList, expectedCharOccurenceList):
    """If two statistical distributions are identical the chi square statistic is 0. The higher number the more they differ.
    @return: Chi-Squared Statistic
    @charOccurenceList: A list with the number of occurences of every character.
    @expectedCharOccurenceList: A list with expected occurences of every character. Ordered in the same way as charOccurenceList.
    """
    sum = 0
    counter = 0
    for element in charOccurenceList:
        sum += getChiSquared(element, expectedCharOccurenceList[counter])
        counter += 1
    return sum
    
def getExpectedCharOccurence(cipherTextLength, alphabetProbabilityTable):
    """
    @cipherTextLength: The length of the cipher text subset we are analysing.
    @return: A frequency count table with the likley number of every character for the language in a text of the cipher text length. The frequency is measured as floats in this table."""
    expectedCharOccurence = []
    occ = 0.0
    for characterProbability in alphabetProbabilityTable:
        occ = characterProbability * cipherTextLength
        expectedCharOccurence = [characterProbability[0], occ]
    return expectedCharOccurence
    
def getCandidateKeyCharacters(cipherText, alphabetProbabilityTable, mPrime):
    """This metod will return most likley characters to be key in a ciphertext for a known key length
    @mPrime: Known keylength
    @cipherText: The encrypted text
    @alphabetProbabilityTable: A table showing the probability for characters in the alphabet used.
    """
    subCipherList = getSubCipherList(cipherText, mPrime)
    subFrequencyCount = []
    for subCipher in subCipherList:
        subFrequencyCount.append(frequencyCounter(cipherText, []))
    #Brutefoce commerce
    return (subFrequencyCount)
    
def test():
    return getCandidateKeyCharacters(textoperations.getFileAsString("duan.encrypt"), getPTableAlphabet("sweletterfrequency.txt"), 11)
    
#Lowest probability for the alphabet. Complete randomness. The probabilty of a coincidence for a uniform random selection from the alphabet.
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