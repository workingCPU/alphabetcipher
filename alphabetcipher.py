
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
	_graphCount = lambda me, c : Counter(c).items() # get word frequency (fq)

	# shared analysis.
	def analyze(me, cstmCiph = "", gw = 1, onlyABC=True) :
		""" gw: max. graph-width: examine n contiguoous chars """

		cipher = me._ciph(cstmCiph)

		for n in range(1, gw+1) :
			fqCiph = me.graphs(cipher, n, onlyABC) # return n-graph list

			fqCiph = me._graphCount(fqCiph) # get frequency of cipher grams.

			fqCiph = [k for k, v in
				sorted(fqCiph, key=lambda item : item[1], reverse=True)]

		print(fqCiph)

		return fqCiph[0] # for now just first element 0.

	# single-char comparison.
	def monograph(me, cstmCiph = "") :
		fqRef = "ETAOINSHRDLCUMWFGYPBKQVXZ" # EN alphabet sorted by fq
		fqCiph = me.analyze(cstmCiph)

		# diff : most frequent chars in cipher text & clear ref
		getDist = lambda c, r : (ord(c) - ord(r)) % 26

		x = 0 # fqRef index
		fqC = fqCiph[0] # increase efficiency, readability.
		fqR = fqRef[x]

		dist = getDist(fqC, fqR) # get real distance
		p = dist + 65 # predict key no.
		pKey = chr(p) # char of predicted key no.

		if fqC < fqR : # direction bwd IF cipher < clear.
			pass # dist = dist-26

		print("Most frequent in ciphertext: ", fqC) # this cipher.
		print("Most frequent in cleartext: ", fqR) # general clear.

		print(f"Predicted key: {pKey} ; ASCII: {p}\n")

		return [p, pKey] # pKey: not for mono but poly, e.g.


	def graphs(me, c, n, onlyABC=True) :
		"""
		Args :
			me : 	class-reference.
			c :	int, ciphertext
			n :	int, width of output graphs
			spaces: bool, exclude / include spaces.
		"""

		# remove all non-alphabetic chars.
		if onlyABC :
			c = [x for x in c if ord(x) >= 65 and ord(x) <= 90]

		g = [] # graphs output list.
		for i in range(n, len(c), 1) :
			g.append("".join(c[i-n:i]))

		return g

	# WORD MODE
	def words() :
		fqWords = me._graphCount(cipher.split(" ")
		pass # tbc


	# GRAPH MODE
	def bigraph(me, cstmCiph = "") :
		fqGraphs = monograph

		biList = ["TH", "IN"]
		distList = []
		for b in biList :
			tmpList = [] # store n dist values for the later tuple.

			for i, c in enumerate(b) :
				tmpList.append(ord(fqGraphs[0][i]) - ord(b[i]))

			distList.append(tuple(tmpList))

		print(distList)

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

		dist = me.monograph(me.cipher)[0]  # get distance / predicted shift.

		for c in me.cipher :
			if ord(c) in range(65, 91) :
				clear += me.decrypt(c, dist)
			else :
				clear += c

		print("Clear", "\n", clear)

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
			dist, keyChar = me.monograph(piece) # get distance / predicted shift.
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
