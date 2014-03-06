# -*- coding: utf-8 -*-
import shlex
from ..keyvalue import KeyValueConfig


class TypeAwareKeyValueConfig(KeyValueConfig):

	def __init__(self, filename, comment_chars=['#', ';']):
		super(TypeAwareKeyValueConfig, self).__init__(filename, comment_chars=comment_chars, values_quoted=False)

	def parse(self, line):
		kvcv = super(TypeAwareKeyValueConfig, self).parse(line)

		if not kvcv:
			return None

		kvcv.value = self.parse_value(kvcv.value)

		return kvcv

	def parse_value(self, s):
		"""
		Implements the parsing of the value potion of a KeyValueConfigValue.

		Returns the typed configuration value. Implemented: string, boolean, int, float, complex.
		The last three use their function to make turn the given string into a value.
		For boolean values the strings "true", "yes" and "on" (case-insensitive) are considered True;
		*only* their direct counterparts ("false", "no", "off") are considered False. Everything else will by
		returned as a string.

		Lists are supported using the [] notation (like python). Each item in the list will by parsed again with
		this function, so the value type of the list items is preserved.
		"""
		if s is None:
			return None

		if self.is_quoted(s):
			# it's a string
			return str(s[1:-1])
		else:
			if s.startswith("[") and s.endswith("]"):
				# it's a list
				return self.parse_list(s.strip().lstrip("[").rstrip("]"))
			else:
				# try each of this function to create a specific type
				for f in [int, float, complex]:
					try:
						return f(s)
					except ValueError:
						pass

				# try to convert it to boolean
				if s.lower() in ["true", "yes", "on"]:
					return True
				elif s.lower() in ["false", "no", "off"]:
					return False

				return s

	def parse_list(self, s):
		parser = shlex.shlex(s)
		parser.whitespace += ","

		l = []
		for x in parser:
			l.append(self.parse_value(x))
		return l