
import sys
from collections import Counter
import os

fqRef = "ETAOINSHRDLCUMWFGYPBKQVXZ" # English alphabet sorted by fq. 

def paramToString(param: str | os.PathLike) -> str :
	if isinstance(param, str) :
		if os.path.isfile(param) : # option file
			with open(param, 'r') as p :
				return p.read()
		else : # option text string
			return str


def analyze() :
	cipher = ""  # encrypted text var.

	if len(sys.argv) < 2 :
		print("Please provide a string parameter.")
		sys.exit(1)
	else :
		param1 = paramToString(sys.argv[1]) # ensure string type.
		cipher = param1.upper() # cipher, case-insensitive.

	fqCiph = dict(Counter(cipher)) # get freuency of cipher letters.

	# [1:] => exclude whitespaces (usually idx 0)
	fqKeys = [k for k, v in
		sorted(fqCiph.items(), key=lambda item : item[1], reverse=True)][1:]


	# get diff of the most frequent chars in cipher text & clear reference
	keyC = lambda c, r : (ord(c) - ord(r)) % 26 + 64 # (one) key character.

	x = 0 # compare idx of fqRef
	fqK = fqKeys[0] # increase efficiency, readability.
	fqR = fqRef[x]

	p = keyC(fqK, fqR) # predict key.
	pChar = chr(p) # respective char.
	dist = p-64 # ascii code to A=1 format.

	if fqK < fqR : # direction bwd IF cipher < clear.
		dist = dist-26

	print("Most frequent in ciphertext: ", fqKeys[0]) # this cipher.
	print("Most frequent in cleartext: ", fqRef[0]) # general clear.

	print(f"Predicted key: {pChar} ; Distance: {dist}")

	return [dist, cipher]

def decryptMono() :
	clear = "" # clear text var.
	dist, cipher = analyze() # get distance / predicted shift.

	clearC = lambda c, k : chr((ord(c) - k - 64) % 26 + 64)  # clear Char.

	for c in cipher :
		if ord(c) in range(65, 91) :
			clear += clearC(c, dist)
		else :
			clear += c

	print(clear)

def main() :
	decryptMono()


if __name__ == "__main__" :
	main()
