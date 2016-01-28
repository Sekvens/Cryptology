Language = "abcdefghijklmnopqrstuvwxyzåäö ,."

def validateString(inputString):
    inputString = list(inputString)
    returnString = ""
    for char in inputString:
        if char not in Language:
            print("Character not recognized: " + char + " Removing the char")
        else:
            returnString = returnString + char
    return returnString

def formatString(inputString):
    inputString.lower()
    return validateString(inputString)

def getFileAsString(fileName):
    with open(fileName, 'r') as fileObject:
        data = fileObject.read()
    return data
    
def test(fileName):
    print(getFileAsStringList(fileName))
    
def test2(fileName):
    print(formatString(getFileAsStringList(fileName)))