
import sys
from collections import Counter
import os
import argparse

class alphaDecrypt() :
	def __init__(me) :
		me.cipher = ""
		me._argParse()

	def _argParse(me) :
		if len(sys.argv) < 2 :
			print("Please provide a parameter.")
			sys.exit(1)
		else :
			param1 = me._paramToString(sys.argv[1])
			me.cipher = param1.upper() # cipher, case-insensitive.

			argList = ["<input>", "--mode", "--keylen"]
			argDesc = [""" <file> or <string> """,
				"""Choose mode: [<mode>]
					mono: Monoalphabetic
					poly: Polyalphabetic""",
				"""Set a key length for poly mode."""]

			parser = argparse.ArgumentParser()
			for i, arg in enumerate(argList) :
				parser.add_argument(arg, help=argDesc[i])

			me.args = parser.parse_args()

	def _paramToString(me, param: str | os.PathLike) -> str :
		if isinstance(param, str) :
			if os.path.isfile(param) : # option file
				with open(param, 'r') as p :
					return p.read()
			else : # option text string
				return str

	_ciph = lambda me, c : c if c != "" else me.cipher

	def analyze(me, cstmCiph = "") :
		cipher = me._ciph(cstmCiph)

		fqRef = "ETAOINSHRDLCUMWFGYPBKQVXZ" # English alphabet sorted by fq. 
		fqCiph = dict(Counter(cipher)) # get freuency of cipher letters.

		# [1:] => exclude whitespaces (usually idx 0)
		fqKeys = [k for k, v in
			sorted(fqCiph.items(), key=lambda item : item[1], reverse=True)]

		# remove all non-alphabetic chars.
		fqKeys = [k for k in fqKeys if ord(k) >= 65 and ord(k) <= 90]

		print(fqKeys)
		# get diff of the most frequent chars in cipher text & clear reference
		keyN = lambda c, r : (ord(c) - ord(r)) % 26 + 65 # (one) key number.
		# 65 = 64 shift + 1 index-correction

		x = 0 # compare idx of fqRef
		fqK = fqKeys[0] # increase efficiency, readability.
		fqR = fqRef[x]

		p = keyN(fqK, fqR) # predict key no.
		pKey = chr(p) # char of predicted key no.

		if fqK < fqR : # direction bwd IF cipher < clear.
			dist = dist-26

		print("Most frequent in ciphertext: ", fqKeys[0]) # this cipher.
		print("Most frequent in cleartext: ", fqRef[x]) # general clear.

		print(f"Predicted key: {pKey} ; ASCII: {p}\n")

		return [p, pKey] # pKey: not for mono but poly, e.g.


	graphCount = lambda me, c : Counter(c) # get word count!


	def graphs(me, c, n, onlyABC=True) :
		"""
		Args :
			me : 	class-reference.
			c :	int, ciphertext
			n :	int, width of output graphs
			spaces: bool, exclude / include spaces.
		"""

		if onlyABC :
			c = c.translate({ord(i): None for i in " ,.()"}) # handle spaces
		print(c)
		g = [] # graphs output list.
		for i in range(2, len(c), 1) :
			g.append(c[i-n:i])

		return g


	def bigraph(me, cstmCiph = "") :
		cipher = me._ciph(cstmCiph) # get cipher.
		fqWords = me.graphCount(cipher.split(" "))

		bigraphs = me.graphs(cipher, 2)
		fqGraphs = me.graphCount(bigraphs)

		print(fqGraphs)

		biList = ["TH", "IN"]
		distList = []
		for b in biList :
			for c in b :
				# distList.append()

	def trigraph(me, cstmCiph = "") :
		cipher = me._ciph(cstmCiph)
		fqWords = me.wordCount(cipher)
		triList = ["THE"]


	# args only for re-usage with poly-alphabetic cipher.
	def decrypt(me, char, dist) :
		clearC = lambda c, k : chr((ord(c) - k) % 26 + 65)  # clear Char.

		return clearC(char, dist)

	def decryptMono(me) :
		clear = "" # clear text to be.

		dist = me.analyze(me.cipher)[0]  # get distance / predicted shift.

		for c in me.cipher :
			if ord(c) in range(65, 91) :
				clear += me.decrypt(c, dist)
			else :
				clear += c

		print(clear)

	def decryptPoly(me, pKeyLen = 6) :
		cipher = me.cipher  # encrypted text var.
		clear = "" # clear text to be.
		key = "" # key to be (captured).

		n = pKeyLen # predicted key length.
		ciphList = ["" for _ in range(n)]

		# slice cipher into n pieces.
		for i in range(0, len(cipher)) :
			ciphList[i % n] += cipher[i]

		# treat each piece of the cipher list as mono-alphabetic.
		distList = []

		for piece in ciphList :
			dist, keyChar = me.analyze(piece) # get distance / predicted shift.
			key += keyChar
			distList.append(dist)

		print(distList, key)

		for i, c in enumerate(cipher) :
			if ord(c) in range(65, 91) :
				clear += me.decrypt(cipher[i], distList[i % n])
			else :
				clear += c

		print(clear)
		triRes = me.bigraph() # no args, just testing.

def main() :
	a = alphaDecrypt()
	if a.args.mode == "poly" :
		if a.args.keylen :

			a.decryptPoly(int(a.args.keylen))
		else :
			a.decryptPoly()
	else :
		# Mono is default.
		a.decryptMono()

if __name__ == "__main__" :
	main()
