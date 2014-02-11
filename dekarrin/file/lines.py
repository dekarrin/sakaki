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
		self.file = open(file, "r")
		self.result = None

	def read(self):
		self.result = self._blank_result()
		for line in self.file:
			line = line.strip()
			if line != '' and line[0] != '#':
				self._read_line(line)
		self.file.close()
		return self.result
	
	def _blank_result(self):
		return None

	def _read_line(self):
		pass

class ConfigReader(_LineReader):
	def __init__(self, file):
		super(ConfigReader, self).__init__(file)

	def _blank_result(self):
		return dict()
		
	def _read_line(self, line):
		name, value = line.split('=', 1)
		name = name.strip()
		value = value.strip()
		if value[0] == '"' and value[-1] == '"':
			self.result[name] = value[1:-1]
		else:
			try:
				self.result[name] = int(value)
			except ValueError:
				try:
					self.result[name] = float(value)
				except ValueError:
					self.result[name] = value
		
class ListReader(_LineReader):
	def __init__(self, file):
		super(ListReader, self).__init__(file)
		
	def _blank_result(self):
		return list()

	def _read_line(self, line):
		if line[0] == '"' and line[-1] == '"':
			self.result.append(line[1:-1])
		else:
			self.result.append(line)

