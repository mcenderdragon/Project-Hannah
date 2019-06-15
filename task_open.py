import interpreter as inter
import helper_aufzaehlung as help_a
import helper_names as help_n

def init(doc, nlp):
	who = []
	where = ""
	for token in doc:
		if token.dep_ == "ROOT":
			for child in token.children:
				print(child.text, "\t", child.dep_, "\t", child.pos_, "\t", child.tag_)
				
				if child.pos_ == "NOUN" and child.dep_ == "oa":
					who.extend(help_a.answer_as_array(child))
				elif child.pos_ == "PROPN" and child.tag_ == "NE":
					who.extend(help_a.answer_as_array(child))
				elif child.pos_ == "ADP" and child.dep_ == "mo":
					where+=inter.as_text(child)
					
	print("who", who, "; where", where)
	who = list(map(help_n.resolve_links, map(help_n.find_files, who)))
	print("who", who)
	
def finish(obj, doc, nlp):
	return;