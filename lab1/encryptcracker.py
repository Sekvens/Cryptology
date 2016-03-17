import textoperations, encrypt
import os
import math
import time

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
    return ((nrOfChar - expectedNrOfChar)*(nrOfChar - expectedNrOfChar))/expectedNrOfChar

def getChiSquaredStatistics(charOccurenceList, expectedCharOccurenceList):
    """If two statistical distributions are identical the chi square statistic is 0. The higher number the more they differ. Theta(|charOccurenceList|)
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
    @return: A frequency COUNT table with the likley number of every character for the language in a text of the cipher text length. The frequency is measured as FLOATs in this table."""
    expectedCharOccurence = []
    occ = 0.0
    for characterProbability in alphabetProbabilityTable:
        occ = characterProbability[1] * cipherTextLength
        expectedCharOccurence.append(occ)
    return expectedCharOccurence
    
def stripCharsFromTable(fTable):
    temp = []
    for el in fTable:
        temp.append(el[1])
    return temp
    
def getKeyChiSquaredStatistics(cipherText, alphabetProbabilityTable, mPrime):
    """This metod will return most likley characters to be key in a ciphertext for a known key length
    @mPrime: Known keylength
    @cipherText: The encrypted text
    @alphabetProbabilityTable: A table showing the probability for characters in the alphabet used.
    """
    subCipherList = getSubCipherList(cipherText, mPrime)
    subFrequencyCount = []
    for subCipher in subCipherList:
        subFrequencyCount.append(frequencyCounter(cipherText, []))
    subCipherCounter = 0
    sCipherLength = len(subCipherList[0])
    alphPTable = debugGetAlphP() #Save alphPTable to reduce IO.
    expCharOccurence = getExpectedCharOccurence(sCipherLength, alphPTable)
    answer = [] #[keyNrCharacter, chiList]
    #Brutefoce starting
    for subCipher in subCipherList:
        chiList = [] #Contains all chi values for this keyCharacter/subCipher
        if(len(subCipher) != sCipherLength):#Only recalculate expectedCharOccurence if subCipher text length differs.
            sCipherLength = len(subCipher)
            expCharOccurence = getExpectedCharOccurence(sCipherLength, alphPTable)
        for i in range(len(alphabet)): #Time-complexity in loop: O(|plainText|+|alphabet|+(|alphabet|*|subCipherText|))
            plainTextCandidateI = encrypt.ceasarCipher(subCipher, i, False)
            chiList.append(getChiSquaredStatistics(stripCharsFromTable(frequencyCounter(plainTextCandidateI, [])), expCharOccurence))
        answer.append([subCipherCounter, chiList])
        subCipherCounter += 1
    return answer
    
def getNMinMax(aList, n, maxFlag):
    maxList = []
    mini = 0
    for elem in aList:
        if(maxFlag):
            if(elem > mini):
                if len(maxList) >= n:
                    maxList.pop(0)
                maxList.append(elem)
                maxList.sort()
                mini = maxList[0]
        else:
            if(elem < mini): #Logic is reversed, mini is actually max and vise versa.
                if len(maxList) >= n:
                    maxList.pop()
                maxList.append(elem)
                maxList.sort()
                mini = maxList[-1]
            elif(len(maxList) < n): #Handling short lists/empty list
                maxList.append(elem)
                maxList.sort()
                mini = maxList[-1]
    return maxList
    
def test():
    chiList = getKeyChiSquaredStatistics(textoperations.getFileAsString("duan.encrypt"), getPTableAlphabet("sweletterfrequency.txt"), 11)
    for key in chiList:
        print("Key for index: ", key[0])
        temp = getNMinMax(key[1], 3, False)
        print("Likley keys:", temp)
        print("Corresponds to the character:", alphabet[key[1].index(temp[1])])
    
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
    
def friedmanTest(encryptedTextFile, minKey, maxKey):
    """Performs a Friedman test on the encrypted contents in a file for keylengths between minKey and maxKey.
    @encryptedTextFile: A file containing the encrypted string in UTF-8 format.
    @minKey: The minimum keylength to test.
    @maxKey: The Maximum key length to test
    @return: A list of Index of Coincidence for every keylength indexed after the keylength where index 0 corresponds to minKey and then step up one for every index occurence up to maxKey."""
    cipherText = textoperations.getFileAsString(encryptedTextFile)
    answers = []
    if(minKey > 0 and maxKey > minKey):
        for i in range(minKey, maxKey+1):
            answers.append(getIndexOfCoincidence(cipherText, i))
    return answers
    
def getKeyCharCandidates(cipherFile, frequencyFile, keyLength, nrOfCandidates):
    """Calculates possible keys
    @cipherFile: The file containing the cipher
    @frequencyFile: A file containing the letter frequency of the alphabet.
    @keyLength: The length of the key.
    @nrOfCandidates: The number of top candidate key caracters for every key possition.
    @return: A list with index position as first element and a list of the top candidate characters in the second element. """
    chiList = getKeyChiSquaredStatistics(textoperations.getFileAsString(cipherFile), getPTableAlphabet(frequencyFile), keyLength)
    for keyChar in chiList:
        top = getNMinMax(keyChar[1], nrOfCandidates, False)
        topAlph = []
        for key in top:
            topAlph.append(alphabet[keyChar[1].index(key)])
        keyChar[1] = topAlph
    return chiList
    
def analysisFreidmanNorm(fileName, maxKey):
    possibleKeyLengths = friedmanTest(fileName, 1, maxKey)
    maxP = getSweProb()
    minP = getSweRandom()
    counter = 1
    for IC in possibleKeyLengths:
        print("Key-length: ", counter, " likleyhood: " , round(((IC - minP) / (maxP - minP) * 100), 2), "%")
        counter += 1
    
def getKeyInFile(fileName, maxKey, nrOfKeys, nrOfCandidateSolutions):
    start = 1
    frequencyTable = "sweletterfrequency.txt"
    possibleKeyLength = friedmanTest(fileName, start, maxKey)
    topKeyCandidates = getNMinMax(possibleKeyLength, nrOfKeys, True)
    topKeys = []
    for keyNr in range(nrOfKeys):
        keyLength = possibleKeyLength.index(topKeyCandidates[nrOfKeys-1-keyNr])+start
        topKeys.append(keyLength)
    #for keyLength in topKeys:
    solutionsForKey = []
    for key in topKeys:
        temp = []
        temp.append(key)
        temp.append(getKeyCharCandidates(fileName, frequencyTable, key, nrOfCandidateSolutions))
        solutionsForKey.append(temp)
    return solutionsForKey
    
#Transforms the output from getKeyInFile to something readable for humans and prints in output.
def prettySolutionPrinter(solutionsForKeys, fileName):
    print("***Presenting solutions for file: ", fileName, "***")
    for keyLengthSolution in solutionsForKeys:
        print("   Presenting candidate keys of length", keyLengthSolution[0])
        topRow = "pos:   "
        CandidateSolution = []
        for i in keyLengthSolution[1][1][1]:
            CandidateSolution.append("")
        for charSolutions in keyLengthSolution[1]:
            topRow += (str)(charSolutions[0])
        word = ""
        for charSolutions in keyLengthSolution[1]:
            for i in range(len(keyLengthSolution[1][1][1])):
                CandidateSolution[i] += (str)(charSolutions[1][i])
        #print(topRow)
        for can in CandidateSolution:
            print("      ", can)

def multicrack(filePath, maxKey, nrOfKeys, nrOfCandidateSolutions):
    for file in textoperations.getFilesInFolder(filePath):
        start_time = time.time()
        prettySolutionPrinter(getKeyInFile(file, maxKey, nrOfKeys, nrOfCandidateSolutions), file)
        print("--- %s seconds ---" % (time.time() - start_time))
        
#Assumes files to aggregate are named text something.
def aggregatecrack(filePath, maxKey, nrOfKeys, nrOfCandidateSolutions):
    cFiles = []
    for file in textoperations.getFilesInFolder(filePath):
        print(file[-12:-8])
        if(file[-12:-8] == "text"):
            cFiles.append(file)
    print(cFiles)