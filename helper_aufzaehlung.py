
def answer_as_array(token, only_childs = False):
	words = []
	if not only_childs:
		words.append(token.text)
	for c in token.children:
		if c.dep_ == "cj":
			words.extend(answer_as_array(c, False))
		elif c.pos_ == "PUNCT" or c.dep_ == "punct":
			continue
		elif c.pos_ == "CONJ" and c.dep_ == "cd":
			words.extend(answer_as_array(c, True))
	
	
	return words