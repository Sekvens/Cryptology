# -*- coding: utf-8 -*-

import os
import re
Alphabet = "abcdefghijklmnopqrstuvwxyzåäö ,."
TAG_RE = re.compile(r'<[^>]+>|\d\.')
SPACE_RE = re.compile(r'[ ][ ]+') #(" +")
NR_RE = re.compile("\d\.")

#Returns the alphabet used.
def getAlphabet():
	return Alphabet
    
#Method borrowed from the StackOverflow user Amber. Changed the reg expression a bit to remove crap from the bible text we use to get a frequency for ., and space
def remove_crap(text):
    temp = TAG_RE.sub('', text)
    temp = SPACE_RE.sub(' ', temp)
    return temp

def specialFormattingBible(inputString):
    """
    Specialized function to remove all non text from the bible that we downloaded.
    @type inputString: String
    @param inputString: Should be a multi line string.
    @return: string
    """
    cleanString = ""
    for row in inputString.split('\n'):
        row = remove_crap(row)
        cleanString = cleanString + row
    return cleanString
    
#This function formats the text by removing chacters not in the alphabet
def validateString(inputString):
    inputString = specialFormattingBible(inputString)
    inputString = list(inputString)
    returnString = ""
    for char in inputString:
        if char in Alphabet:
            returnString = returnString + char
    return returnString

#Lowercase and removes non alphabet characters
def formatString(inputString):
    #inputString.lower()
    return validateString(inputString.lower())

#Takes a filenName as a string and returns the contents as a string. Not Safe
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