import textoperations
import os

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
    
def transformFTable(frequencyTable):
    sum = 0
    for charContrainer in frequencyTable:
        sum = sum + charContrainer[1]
    for charContrainer in frequencyTable:
        charContrainer[1] = round((charContrainer[1] / sum), 3)
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
    
def getCurrentPath():
    return os.path.dirname(os.path.realpath(__file__))
    
def getIndexOfCoincidence(cipherText):
    """
    This calculates K_o or what's called IC(x^j). 
    """
    N = len(cipherTextSubset)
    cipherCharFrequency = frequencyCounter(cipherText, [])
    for i in range(len(alphabet)):
        #Occurence of character i
        fxj = cipherCharFrequency[i][1]
        #Replace occurence with ic(char_i)
        cipherCharFrequency[i][1] = (fxj*(fxj-1))/(N*(N-1))
    
def getAverageIndexOfCoincidence(icTable):
    """This is the likleyhood that two random elements are identical. It's an average of all index of coincidence for a string."""
    i = 0
    sum = 0
    for tuple in icTable:
        sum += tuple[1]
        i += 1
    return ((1/i) * sum)
    
#Lowest IC for the alphabet. Complete randomness.
def getAlphabetICRandom(alph):
    return 1/len(alph)
    
def getLanguageFrequency():
    print("todo later")
    
def friedmanTest(encryptedText):
    alphabetLength = len(textoperations.getAlphabet())
    probability_char