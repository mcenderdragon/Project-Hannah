import spacy
import interpreter as inter
nlp = spacy.load("de_core_news_md")
doc = nlp(u"Das ist ein Satz.")
print("Load Completed")
while True:
	text = input(">")
	doc = nlp(text)
	inter.basic_input(doc, nlp)