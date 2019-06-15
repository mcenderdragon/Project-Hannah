import json
import spacy

def find_root(doc: spacy.tokens.doc.Doc) -> spacy.tokens.token.Token:
	for e in doc:
		if e.dep_ == "ROOT":
			return e
	return None


def basic_input(doc, nlp):
	print("got '", doc, "'")
	root = find_root(doc)
	print("root is '", root, "'")
	
	if root != None:
		task = get_task(root.text, nlp, True)
		if task != None:
			try:
				modul = __import__(task)
				obj = modul.init(doc, nlp)
				modul.finish(obj, doc, nlp)
			except:
				print("Error beim Versuch das Modul '", task, "' zu laden!")

tasks = None


def get_task(text, nlp, create_new):
	global tasks
	if tasks is None:
		try:
			with open('tasks.json') as handle:
				tasks = dict(json.loads(handle.read()))
		except FileNotFoundError:
			tasks = dict()
		except json.decoder.JSONDecodeError:
			tasks = disct()
	
	task = tasks.get(text)
	if task != None:
		return task
	elif create_new:
		return new_task(text, nlp)
	else:
		return None


def new_task(text, nlp):
	global tasks
	answ = what_is(text, nlp)
	print(answ)
	existing = get_task(answ, nlp, False)
	
	if existing != None:
		print("Existierende Aufgabe gefunden ", existing)
		define_task(text, existing)
		return existing
	else:
		print("Neue Aufgaben definition")
		try:
			module = __import__(answ)
			define_task(text, answ)
			return answ
		except ImportError:
			print("Kein Module mit dem Namen '", answ, "' gefunden!")
			return None
		

def define_task(text, task_name):
	global tasks
	if tasks is None:
		try:
			with open('tasks.json') as handle:
				tasks = dict(json.loads(handle.read()))
		except FileNotFoundError:
			tasks = dict()
		except json.decoder.JSONDecodeError:
			tasks = disct()
	
	tasks[text] = task_name
	print("Neues modul ", text, "=", task_name)
	
	with open('tasks.json', 'w') as fp:
		json.dump(tasks, fp)
	print("modul liste gespeichert")


def as_text(entry):
	return as_text_without(entry, [], False)

def as_text_without(entry, ignore, article):
	str = dict()
	if entry.i in ignore:
		return ""
	elif not article and entry.tag_ == "ART":
		return ""
	
	str[entry.i] = entry.text
	for c in entry.children:
		if c.i in ignore:
			continue
		elif not article and c.tag_ == "ART":
			continue
		
		str[c.i] = as_text_without(c, ignore, article)
	
	s = ""
	for c in str: 
		if len(s)>0 and s[-1] != " ":
			s += " "
		s += str[c]
	return s

def what_is(text, nlp):
	text = text.strip()
	print("Was ist '", text, "'")
	answ = nlp(input(">"))
	root = find_root(answ)
	if root.text == "ist":
		elm = None
		for child in root.children:
			if child.pos_ == "NOUN" and child.dep_ == "pd":
				elm = child
		if elm != None:
			return as_text(elm)
		else:
			childs = []
			for child in root.children:
				if child.pos_ == "PUNCT":
					continue
				elif child.pos_ == "PRON" and child.dep_ == "sb":
					continue
				elif child.lower_ == text.lower():
					continue
				else:
					childs.append(child)
			
			if len(childs) == 1:
				return as_text(childs[0])
			else:
				while True:
					for c in childs: print("or", c)
					print("Bounds ", 0, "-", len(childs)-1)
					pos = int(input())
					if pos > 0 and pos < len(childs):
						return as_text(childs[pos])
					else:
						print("Out of bounds ", 0, "-", len(childs))
	else:
		gleich = False
		wie = False
		ignore = []
		
		for c in root.children:
			if c.lemma_ == "wie":
				wie = True
				ignore.append(c.i)
			elif c.lemma_ == "derselbe":
				gleich = True
				ignore.append(c.i)
			elif c.lemma_ == "gleichen" or c.lemma_ == "gleich":
				gleich == True
				ignore.append(c.i)
		if gleich and wie:
			return as_text_without(root, ignore)
		else:
			return as_text(root)