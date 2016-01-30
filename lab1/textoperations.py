import os
Alphabet = "abcdefghijklmnopqrstuvwxyzåäö ,."

#Returns the alphabet used.
def getAlphabet():
	return Alphabet

#This function formats the text by removing chacters not in the alphabet
def validateString(inputString):
    inputString = list(inputString)
    returnString = ""
    for char in inputString:
        if char not in Alphabet:
            print("Character not recognized: " + char + " Removing the char")
        else:
            returnString = returnString + char
    return returnString

#Lowercase and removes non alphabet characters
def formatString(inputString):
    #inputString.lower()
    return validateString(inputString.lower())

#Takes a filenName as a string and returns the contents as a string.
def getFileAsString(fileName):
    with open(fileName, 'r', encoding='utf-8') as fileObject:
        data = fileObject.read()
    return data
    
#The input for the encryption algorithm.	
def getFormattedStringFromFile(fileName):
	return formatString(getFileAsString(fileName))
    
#Write string to file
def printOutputToFile(fileName, stringToPrint):
    if(os.path.exists(fileName)):
        with open(fileName, 'w', encoding='utf-8') as outputFile:
            outputFile.write(stringToPrint)
        print("File written successfully")
    else:
        print("Output file not found.")