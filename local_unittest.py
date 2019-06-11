import unittest

import spacy
import helper_aufzaehlung as help_a


nlp = None

class TestBasicInput(unittest.TestCase):
	
	nlp = None
	
	def test_0(self):
		self.__class__.nlp = spacy.load("de_core_news_md")
		print("Model loaded")
	
	def test_aufzaehlung(self):
		doc = self.__class__.nlp(u"Starte Eclipse, Git Extensions und Gimp in Code.")
		self.assertEqual(help_a.answer_as_array(doc[1]), ["Eclipse", "Git Extensions", "Gimp"], "Should be [Eclipse, Git Extensions, Gimp]")
	
	def test_adjectives(self):
		doc = self.__class__.nlp(u"Starte das rote Eclipse, das schwere große Git Extensions und das nützliche GNU Image Manipulation Programm.")
		self.assertEqual(help_a.answer_as_array(doc[3]),['rote Eclipse', 'das schwere große Git Extensions', 'nützliche GNU Image Manipulation Programm'], "adjective+Word extration failed.")


if __name__ == '__main__':
	print("Starting unittest")
	unittest.main()
