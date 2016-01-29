import textoperations
import sys
import os
import codecs

nonSafeFileName = ""
plainText = ""
key = ""
encryptedText = ""
nonSafeOutput = ""

if(len(sys.argv) >= 2):
    nonSafeFileName = sys.argv[1]
    plainText = textoperations.getStringForEncryption(nonSafeFileName)
    
if(len(sys.argv) >= 3):
    nonSafeKeyFile = sys.argv[2]
    key = textoperations.getStringForEncryption(nonSafeKeyFile)
    
if(len(sys.argv) == 4):
    nonSafeOutput = sys.argv[3]
    
#In python a string is a list. By calling Alphabet[x] we get the character for that number sequence. This we can use as our character -> number mapping.
Alphabet = textoperations.getAlphabet()

print("Filename given is: " + nonSafeFileName)

def encrypt2(plaintext):
    plaintextIndex = 0
    keyLength = len(key)
    encryptedText = ""
    if(keyLength == 0):
        return "Key missing"
    for char in plaintext:
        #calculate what key character to use and look up the number in the alphabet
        keyInteger = Alphabet.index(key[plaintextIndex % keyLength])
        #Fetching the current char's integer 
        plainTextInteger = Alphabet.find(char)
        plaintextIndex += 1
        print(plainTextInteger)
        print(keyInteger)
        encryptedChar = Alphabet[(plainTextInteger + keyInteger) % len(Alphabet)]
        encryptedText = encryptedText + encryptedChar
    return encryptedText

def decrypt(plaintext):
    plaintextIndex = 0
    keyLength = len(key)
    encryptedText = ""
    if(keyLength == 0):
        return "Key missing"
    for char in plaintext:
        #calculate what key character to use and look up the number in the alphabet
        keyInteger = Alphabet.index(key[plaintextIndex % keyLength])
        #Fetching the current char's integer 
        plainTextInteger = Alphabet.find(char)
        plaintextIndex += 1
        print(plainTextInteger)
        print(keyInteger)
        encryptedChar = Alphabet[(plainTextInteger - keyInteger) % len(Alphabet)]
        encryptedText = encryptedText + encryptedChar
    return encryptedText    
    
if(plainText != ""):
    print("Found plaintext, performing encryption.")
    print("plaintext is:" )
    if(os.path.exists(nonSafeOutput)):
        with open(nonSafeOutput, 'w', encoding='utf-8') as outputFile:
            encryptionString = textoperations.getStringForEncryption(nonSafeFileName)
            outputFile.write(encrypt2(encryptionString))
        print("File written successfully.")
    else:
        print("Output not found for: " + nonSafeOutput)