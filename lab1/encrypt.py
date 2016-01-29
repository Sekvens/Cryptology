import textoperations
import sys

nonSafeFileName = ""
plainText = ""
key = ""
encryptedText = ""
if(len(sys.argv) >= 2):
    nonSafeFileName = sys.argv[1]
    plainText = textoperations.getStringForEncryption(nonSafeFileName)
    
if(len(sys.argv) == 3):
    nonSafeKeyFile = sys.argv[2]
    key = textoperations.getStringForEncryption(nonSafeKeyFile)
    
#In python a string is a list. By calling Alphabet[x] we get the character for that number sequence. This we can use as our character -> number mapping.
Alphabet = textoperations.getAlphabet()

print("Filename given is: " + nonSafeFileName)

def encrypt2(plaintext):
    plaintextIndex = 0
    keyLength = len(key)
    if(keyLength == 0):
        return "Key missing"
    for char in plaintext:
        #calculate what key character to use and look up the number in the alphabet
        keyInteger = Alphabet.index(key[plaintextIndex % keyLength+1])
        #Fetching the current char's integer representative
        plainTextInteger = Alphabet.index[char]
        plaintextIndex += 1
        encryptedChar = Alphabet[(plainTextInteger + keyInteger) % Alphabet]
        encryptedText += encryptedChar
    return encryptedText

if(plainText != ""):
    print("Found plaintext, performing encryption")
    print(encrypt2(plainText))
    