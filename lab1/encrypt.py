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

if(plaintext != ""):
	plaintext = textoperations.getStringForEncryption(fileName)
	for char in plaintext:
		