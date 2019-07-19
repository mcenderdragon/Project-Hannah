
import os
import struct

def get_desktop():
	return os.path.expanduser("~/Desktop")
	
def get_user():
	return os.path.expanduser("~")


def get_startmenu_paths():
	pathA = os.getenv("APPDATA") +"\\Microsoft\\Windows\\Start Menu"
	pathB = os.getenv("ProgramData") + "\\Microsoft\\Windows\\Start Menu\\"
	return [pathA, pathB]

def get_search_path():
	paths = []
	paths.append(get_desktop())
	paths.append(get_user())
	paths.extend(get_startmenu_paths())
	return paths

def find_files(name, path_list = None):
	result = []
	if path_list is None:
		path_list = get_search_path()
	
	for path in path_list:
		for root, dirs, files in os.walk(path):
			for file in files:
				if is_searched(file, name):
					result.append(root + "/" + file)
	
	return result


def is_searched(file_name, searched):
	file_name = file_name.lower()
	searched = searched.lower()
	return searched in file_name

def resolve_links(path_list):
	return list(map(resolve_link, path_list))

def resolve_link(path):
	if not path.endswith(".lnk"):
		return path
	
	target = ''
	
	with open(path, 'rb') as stream:
		content = stream.read()
		# skip first 20 bytes (HeaderSize and LinkCLSID)
		# read the LinkFlags structure (4 bytes)
		lflags = struct.unpack('I', content[0x14:0x18])[0]
		position = 0x18
		# if the HasLinkTargetIDList bit is set then skip the stored IDList 
		# structure and header
		if (lflags & 0x01) == 1:
			position = struct.unpack('H', content[0x4C:0x4E])[0] + 0x4E
		last_pos = position
		position += 0x04
		# get how long the file information is (LinkInfoSize)
		length = struct.unpack('I', content[last_pos:position])[0]
		# skip 12 bytes (LinkInfoHeaderSize, LinkInfoFlags, and VolumeIDOffset)
		position += 0x0C
		# go to the LocalBasePath position
		lbpos = struct.unpack('I', content[position:position+0x04])[0]
		position = last_pos + lbpos
		# read the string at the given position of the determined length
		size= (length + last_pos) - position - 0x02
		temp = struct.unpack('c' * size, content[position:position+size])
		target = ''.join([chr(ord(a)) for a in temp])
	return target