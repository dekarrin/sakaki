"""Classes for reading plaintext files that consist of several entries separated
by line.

All files read by classes in this module follow some additional rules. The lines
from a file being read are processed one at a time. Each line is stripped of
leading and trailing whitespace. If the first non-whitespace character is '#',
the line is considered a comment and is ignored. If the stripped line is empty,
the line is considered empty and is ignored.

Some file formats consist of different values Double quotes may be used to
encapsulate leading and trailing whitespace that is to be preserved.
"""

class _LineReader(object):
	"""Abastract base class for reading plaintext files made up of lines."""
	
	def __init__(self, file):

class ConfigReader(object):
	def __init__(self, file):
		self.file = open(file, "r")
		self.config = None
		
	def read(self):
		self.config = dict()
		for line in self.file:
			line = line.strip()
			if line != '' and line[0] != '#':
				self.read_config_line(line)
		self.close()
		return self.config
		
	def read_config_line(self, line):
		name, value = line.split('=', 1)
		name = name.strip()
		value = value.strip()
		if value[0] == '"' and value[-1] == '"':
			self.config[name] = value[1:-1]
		else:
			try:
				self.config[name] = int(value)
			except ValueError:
				try:
					self.config[name] = float(value)
				except ValueError:
					self.config[name] = value
			
	def close(self):
		self.file.close()
		
class ListReader(object):
	def __init__(self, file):
		self.file = open(file, "r")
		self.config = None
		
	def read(self):
		self.list = list()
		for line in self.file:
			line = line.strip()
			if line.strip()[0] == '"' and line.strip[-1] == '"':
				self.list.append(line.strip()[1:-1])
			else:
				self.list.append(line.strip())
		self.close()
		return self.list
		
	def close(self):
		self.file.close()