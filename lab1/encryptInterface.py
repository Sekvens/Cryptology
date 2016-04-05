import argparse
import encrypt

parser = argparse.ArgumentParser(description="This is a CLI for cryptology lab 1. Use UTF-8 encoding for all input and output.")

parser.add_argument("input", help="The input textfile that should be encrypted or decrypted.", )
parser.add_argument("keyfile", help="A file containing the key used by the algorithm.")
parser.add_argument("output", help="The output file where the result will be written.")
parser.add_argument("-d", "--decrypt", help="If set the program will decrypt instead of encrypt", action="store_true")

args = parser.parse_args()

if(args.decrypt):
    encrypt.doDecrypt(args.input, args.keyfile, args.output)
    print("Decrypting" + args.input)
else:
    encrypt.doEncrypt(args.input, args.keyfile, args.output)
    print("Encrypting" + args.input)