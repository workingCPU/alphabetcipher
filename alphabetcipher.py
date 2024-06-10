
import sys
from collections import Counter
import os
import argparse

class alphaDecrypt() :
	def __init__(me) :
		me.cipher = ""
		me._argParse()
		me.fqRef = "ETAOINSHRDLCUMWFGYPBKQVXZ" # EN ABC sorted by fq

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
					poly: Polyalphabetic
					polyN: Polyalphabetic ngram""",
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


	def grams(me, props) :
		"""
		Args :
			me : 	class-reference.
			props: contains all necessary properties
		"""
		c, n, onlyABC = props.values() # unpack valuues, c=cipher.
		
		# remove all non-alphabetic chars.
		if onlyABC :
			c = [x for x in c if ord(x) >= 65 and ord(x) <= 90]

		g = [] # grams output list.
		for i in range(n, len(c), 1) :
			g.append("".join(c[i-n:i]))

		return g

	_gramCount = lambda me, c : Counter(c).items() # get word frequency (fq)

	# shared analysis.
	def analyze(me, props : dict) :
		""" props: contains all necessary properties """

		fqCiph = me.grams(props) # return n-gram list
		fqCiph = me._gramCount(fqCiph) # get frequency of cipher grams.

		fqCiph = [k for k, v in
			sorted(fqCiph, key=lambda item : item[1], reverse=True)]

		print(fqCiph)

		return fqCiph # for now just first element 0.

	# single-char comparison.
	def monogram(me, props : dict) :
		""" props: contains all necessary properties """

		# r, fqR = props.pop("r"), props.pop("fqRef") # leave r and...
		r, fqR = [props.pop(x) for x in ["r", "fqRef"]]

		fqCiph = me.analyze(props) # travel to "analyze".

		# diff : most frequent chars in cipher text & clear ref
		getDist = lambda c, r : (ord(c) - ord(r)) % 26

		n = props['n'] # fqRef index range, upper limit = ngram-width
		
		fqC = fqCiph[0] # increase efficiency, readability.
		
		# store all keys, dists && tmps respectively.
		tmp, keyList, distTmp, distList = [], [], [], []
					
		for i in range(r) :
			fq = fqR[i] # one reference fq token
			for g in range(n) :
				dist = getDist(fqC[g], fq[g]) # get real distance
				p = dist + 65 # predict key no.
				
				distTmp.append(dist) # store dist.								
				tmp.append(p) # store predicted no.
		
			distList.append(distTmp)
			pKeys = [(p, chr(p)) for p in tmp] # store keys & chars
			keyList.append(pKeys)
			tmp, distTmp = [], [] # reset tmps
		
		keys0 = keyList[0]
		dist0 = distList[0]
				
		print("Most frequent in ciphertext: ", fqC) # this cipher.
		print("Most frequent in cleartext: ", fqR) # general clear.

		print(f"Predicted keys / ASCII: {keys0} ; distance: {dist0}\n")

		return pKeys # pKey: not for mono but poly, e.g.

	# WORD MODE
	def words() :
		fqWords = me._gramCount(cipher.split(" "))
		pass # tbc


	# GRAM MODE
	def ngram(me, props) :
		biList = ["TH", "IN"]				
		triList = ["THE"]
		nList = []

		if props["n"] == 2 :
			nList = biList
		elif props["n"] == 3 :
			nList = triList

		props["fqRef"] = nList # change 
		return me.monogram(props)		

	def mkDict(me, ciph, n, onlyABC, r, ref) :
		"""
		Params :
			cipher :	[str] ciphertext.
			n : 		[int] width of the n-gram.
			onlyABC :	[bool] excl. / incl. non-ABC chars.
			r :			[int] research-depth, # of clear-ref grams
			fqRef :		[list] clear-ref frequencies
		"""

		return dict({"cipher": ciph, "n": n, "onlyABC": onlyABC,
					"r": r, "fqRef": ref})


	# args only for re-usage with poly-alphabetic cipher.
	def decrypt(me, char, dist) :
		clearC = lambda c, k : chr((ord(c) - k) % 26 + 65) # clear Char.

		return clearC(char, dist)

	def decryptMono(me) :
		clear = "" # clear text to be.

		# monogram properties.		
		params = me.mkDict(me.cipher, 1, True, 1, me.fqRef)

		dist = me.monogram(params)[0][0] # get distance / predicted shift.
		print("Dist:", dist)

		for c in me.cipher :
			if ord(c) in range(65, 91) :
				clear += me.decrypt(c, dist)
			else :
				clear += c

		print("Cleartext:", "\n", clear)

	def decryptPolyMono(me, pKeyLen = 6) :		
		""" Description:
				Polyalphabetic monogram-based mode.
		"""
		clear = "" # clear text to be.
		key = "" # key to be (captured).
		n = pKeyLen # predicted key length.
		
		ciphList = ["" for _ in range(n)] # cipher to n pieces

		for i in range(0, len(me.cipher)) :
			ciphList[i % n] += me.cipher[i] # and store them.

		# treat each piece of the cipher list as mono-alphabetic.
		distList = []

		for piece in ciphList :
			# monogram properties.
			params = me.mkDict(piece, 1, True, 1, me.fqRef)
			
			dist, keyChar = me.monogram(params)[0] # distance / predicted shift.

			key += keyChar
			distList.append(dist)

		print(distList, key)

		for i, c in enumerate(me.cipher) :
			if ord(c) in range(65, 91) :
				clear += me.decrypt(me.cipher[i], distList[i % n])
			else :
				clear += c

		print(clear)

	def decryptPolyNgrams(me, pKeyLen=6) :
		""" Description:
				Polyalphabetic ngram-based mode."""

		# monogram properties.
		n = pKeyLen
		params = me.mkDict(me.cipher, n, True, 1, me.fqRef)
		nDist = me.ngram(params) # load bigram, get dists.
		print(nDist)
		
		# decrypt.
		tmpClear = "" # ngram results.
		nClear = [] # store ngram results.

		for i, c in enumerate(me.cipher) :			
			if ord(c) in range(65, 91) :
				tmpClear += me.decrypt(c, nDist[i % n][0])
			else :
				tmpClear += c

		nClear.append(tmpClear)

		print(f"Cleartext ({n}-gram):\n", nClear[0])

def argDecode(a) :	
	keylen = a.args.keylen

	def keyCheck(n) :
		if int(keylen) < n :
			print(f"For this mode, key length has to be >= {n}.")
			sys.exit(1)

	keyCheck(1) # no keys < 1 for anyone.

	if a.args.mode == "poly" :
		if keylen :			
			a.decryptPolyMono(int(a.args.keylen))
		else :
			a.decryptPolyMono()
	elif a.args.mode == "polyN" :		
		if keylen :						
			keyCheck(2) # no keys < 2 for anyone.
			a.decryptPolyNgrams(int(a.args.keylen))
		else :
			a.decryptPolyNgrams()
	else :
		# Mono is default.
		a.decryptMono()


def main() :
	a = alphaDecrypt()
	argDecode(a)

if __name__ == "__main__" :
	main()
