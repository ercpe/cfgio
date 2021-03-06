# -*- coding: utf-8 -*-
import shlex
from ..keyvalue import KeyValueConfig


class TypeAwareKeyValueConfig(KeyValueConfig):

	def __init__(self, filename=None, **kwargs):
		kwargs['values_quoted'] = True
		super(TypeAwareKeyValueConfig, self).__init__(filename, **kwargs)

	def parse(self, line):
		kvcv = super(TypeAwareKeyValueConfig, self).parse(line)

		if not kvcv:
			return None

		kvcv.value = self.parse_value(kvcv.key, kvcv.value)

		return kvcv

	def parse_value(self, key, value):
		"""
		Implements the parsing of the value potion of a KeyValueConfigValue.

		Returns the typed configuration value. Implemented: string, boolean, int, float, complex.
		The last three use their function to make turn the given string into a value.
		For boolean values the strings "true", "yes" and "on" (case-insensitive) are considered True;
		*only* their direct counterparts ("false", "no", "off") are considered False. Everything else will by
		returned as a string.

		Lists are supported using the [] notation (like python). Each item in the list will by parsed again with
		this function, so the value type of the list items is preserved.

		Subclasses can override this method to implement an even more specialized value conversion.

		:param key: The key
		:param value: The value
		"""
		if value is None:
			return None

		if self.is_quoted(value):
			# it's a string
			return str(value[1:-1])

		if value.startswith("[") and value.endswith("]"):
			# it's a list
			return self.parse_list(key, value.strip().lstrip("[").rstrip("]"))

		# try each of this function to create a specific type
		for f in [int, float, complex]:
			try:
				return f(value)
			except ValueError:
				pass

		# try to convert it to boolean
		if value.lower() in ["true", "yes", "on"]:
			return True
		elif value.lower() in ["false", "no", "off"]:
			return False

		return value

	def parse_list(self, key, value):
		"""
		Parses a string into a list using the shlex module. Each list item is parsed again with self.parse_value
		to implement a typed list.
		:param value:the string to parse
		:return: a list
		"""

		if not value:
			return []

		parser = shlex.shlex(value)
		parser.whitespace += ","
		parser.wordchars += "."

		l = []
		for x in parser:
			l.append(self.parse_value(key, x))
		return l

	def format(self, value):
		value_string = None

		if isinstance(value.value, list):
			value_string = "[ %s ]" % ', '.join([self.format_value(x) for x in value.value])
		else:
			value_string = self.format_value(value.value)

		return "%s%s%s" % (value.key, self.separator, value_string)

	def format_value(self, value):
		if isinstance(value, str):
			return '"%s"' % value.replace('"', '\"') # FIXME: Find a better way to quote quotes

		if isinstance(value, bool):
			return str(value).lower()

		if isinstance(value, (float, int, complex)):
			return str(value)

		return str(value)