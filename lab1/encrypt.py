import textoperations
import sys

nonSafeFileName = ""
if(len(sys.argv) == 2):
	nonSafeFileName = sys.argv[1]
	
#In python a string is a list. By calling Alphabet[x] we get the character for that number sequence. This we can use as our character -> number mapping.
Alphabet = textoperations.getAlphabet()

plainText = ""
key = ""
encryptedText = ""

print("Filename given is: " + nonSafeFileName)

def encrypt(plaintext):
	plaintextIndex = 0
	keyLength = len(key)
	for char in plaintext:
		#calculate what key character to use and look up the number in the alphabet
		keyInteger = Alphabet.index(key[plaintextIndex % keyLength])
		#Fetching the current char's integer representative
		plainTextInteger = Alphabet.index[char]
		plaintextIndex += 1
		encryptedChar = Alphabet[(plainTextInteger + keyInteger) % Alphabet]
		encryptedText += encryptedChar
	return encryptedText
		
if(plaintext != ""):
	plaintext = textoperations.getStringForEncryption(fileName)
	print encrypt(plaintext)