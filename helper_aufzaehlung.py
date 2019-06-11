
def answer_as_array(token, only_childs = False):
	words = []
	if not only_childs:
		words.append(combine_adjectives_as_text(token))
	for c in token.children:
		if c.dep_ == "cj":
			words.extend(answer_as_array(c, False))
		elif c.pos_ == "PUNCT" or c.dep_ == "punct":
			continue
		elif c.pos_ == "CONJ" and c.dep_ == "cd":
			words.extend(answer_as_array(c, True))
	
	
	return words



def combine_adjectives(token):
	words = dict()
	words[token.i] = token.text
	for c in token.children:
		if token.pos_ == "NOUN" or token.pos_ == "PROPN":
			if c.dep_ == "nk" and not c.pos_ == "DET":
				words = {**words, **combine_adjectives(c)}
			if c.dep_ == "pnc" and (c.pos_ == "NOUN" or c.pos_ == "PROPN"):
				words = {**words, **combine_adjectives(c)}
		elif token.pos_ == "ADJ":
			if c.dep_ == "mo":
				words = {**words, **combine_adjectives(c)}
	return words

def combine_adjectives_as_text(token, seperator = " "):
	d = combine_adjectives(token)
	print(d)
	s = ""
	for c in sorted(d.keys()): 
		if len(s)>0 and s[-1] != seperator:
			s += seperator
		s += d[c]
	return s