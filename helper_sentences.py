#doc.sents returns spans
#span.root

import spacy
from typing import List

def split_sentences(doc : spacy.tokens.doc.Doc) -> List[spacy.tokens.span.Span]:
	parts = []
	for s in doc.sents:
		partts.append(s)
		
	return parts