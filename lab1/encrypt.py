import textoperations
import sys
import os
import codecs
    
#In python a string is a list. By calling Alphabet[x] we get the character for that number sequence. This we can use as our character -> number mapping.
Alphabet = textoperations.getAlphabet()

def vigenereCipher(inputString, keyString, encrypt):
    """
    Cipher a string with the Vigenere cipher.
    
    @type inputString: String
    @type inputString: The text to encrypt or decrypt.
    @type keyString: String
    @type keyString: The key for the cipher.
    @type encrypt: Boolean
    @param encrypt: If the algorithm should encrypt or decrypt.
    @rtype: String
    """
    inputIndex = 0
    keyLength = len(keyString)
    outText = ""
    if(keyLength == 0):
        print("Key missing")
        return "Key missing"
    for char in inputString:
        #calculate what key character to use and look up the number in the alphabet
        keyInteger = Alphabet.index(keyString[inputIndex % keyLength])
        #Fetching the current char's integer 
        inputInteger = Alphabet.find(char)
        inputIndex += 1
        if(encrypt):
            outChar = Alphabet[(inputInteger + keyInteger) % len(Alphabet)]
        else:
            outChar = Alphabet[(inputInteger - keyInteger) % len(Alphabet)]
        outText = outText + outChar
    return outText

def encrypt(plaintext, key):
    return vigenereCipher(plaintext, key, True)

def decrypt(encryptedText, key):
    return vigenereCipher(encryptedText, key, False)
    
def doCrypt(inFile, keyFile, outFile, encryptB):
    if(os.path.exists(inFile) and os.path.exists(keyFile)):
        inString = textoperations.getFormattedStringFromFile(inFile)
        keyString = textoperations.getFormattedStringFromFile(keyFile)
        outString = ""
        if(encryptB):
            outString = encrypt(inString, keyString)
        else:
            outString = decrypt(inString, keyString)
        textoperations.printOutputToFile(outFile, outString)
    else:
        print("Didn't find the keyfile or the inFile file.")
    
def doEncrypt(plaintextFile, keyFile, outFile):
    """
    Takes text from a file and writes a encrypted version of it in another file.
    @type plaintextFile: String
    @param plaintextFile: A string with a filename containing the plaintext.
    @type keyFile: String
    @param keyFile: A string with a filename containing the key.
    @type outFile: String
    @param outFile: A string with a filename where the result will be written.
    """
    doCrypt(plaintextFile, keyFile, outFile, True)
        
def doDecrypt(encryptedTextFile, keyFile, outFile):
    """
    Takes an encryped text from a file and writes a decrypted version in another file.
    @type encryptedTextFile: String
    @param encryptedTextFile: A string with a filename containing the encrypted text.
    @type keyFile: String
    @param keyFile: A string with a filename containing the key.
    @type outFile: String
    @param outFile: A string with a filename where the result will be written.
    """
    doCrypt(encryptedTextFile, keyFile, outFile, False)