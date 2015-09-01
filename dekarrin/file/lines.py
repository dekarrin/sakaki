"""Classes for reading plaintext files that consist of several entries separated
by line.

All files read by classes in this module follow some additional rules. The lines
from a file being read are processed one at a time. Each line is stripped of
leading and trailing whitespace. If the first non-whitespace character is '#',
the line is considered a comment and is ignored. If the stripped line is empty,
the line is considered empty and is ignored.

Some file formats consist of different values. Double quotes may be used to
encapsulate leading and trailing whitespace that is to be preserved.
"""

import json

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
		self._on_close()
		return self.result
	
	def _blank_result(self):
		return None

	def _read_line(self):
		pass

	def _on_close(self):
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

class ControlSchemeReader(_LineReader):
	def __init__(self, file):
		super(ControlSchemeReader, self).__init__(file)

	def _blank_result(self):
		return {'attributes': dict(), 'rules': list()}

	def _read_line(self, line):
		if '=' in line:
			self._read_attr_line(line)
		elif '->' in line:
			self._read_production_line(line)

	def _read_attr_line(self, line):
		name, value = line.split('=', 1)
		name = name.strip()
		value = value.strip()
		if value[0] == '"' and value[-1] == '"':
			self.result['attributes'][name] = value[1:-1]
		else:
			try:
				self.result['attributes'][name] = int(value)
			except ValueError:
				try:
					self.result['attributes'][name] = float(value)
				except ValueError:
					self.result['attributes'][name] = value

	def _read_production_line(self, line):
		key, productions_str = line.split("->", 1)
		key = key.strip()
		productions_str = productions_str.strip()
		raw_key_keys = rule.split(' ')
		keys = []
		for k in raw_rule_keys:
			if k.strip() is not "":
				keys.append(k.strip())
		prod_lists = productions_str.split(',')
		productions = []
		for prod_list in prod_lists:
			prod_list = prod_list.strip()
			raw_prod_keys = prod_list.split(' ')
			prod_keys = []
			for key in raw_prod_keys:
				if key.strip() is not "":
					prod_keys.append(key.strip())
			productions.append(prod_keys)
		self.result['rules'].append((keys, productions))
		
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
