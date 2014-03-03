# -*- coding: utf-8 -*-
from cfgio.base import ReadConfig, ConfigValueBase, WriteConfig


class KeyValueConfigValue(ConfigValueBase):

	def __init__(self, *args):
		super(KeyValueConfigValue, self).__init__(args[0])
		self.value = args[1]

	def __repr__(self):
		return "%s=%s" % (self.key, self.value)


class KeyValueConfig(WriteConfig):
	"""Key-Value configuration file format. Key-value pairs are store line by line. Values may be quoted"""

	quote_chars = ['"', "'"]

	def __init__(self, filename, separator="=", values_quoted=False):
		super(KeyValueConfig, self).__init__(filename)
		self.values_quoted = values_quoted
		self.separator = separator

	def parse(self, line):
		if not self.separator in line or len(line[:line.index(self.separator)].strip()) == 0:
			return None

		key = line[:line.index(self.separator)].strip()
		value = line[line.index(self.separator)+1:].strip()

		if self.values_quoted and value and (value[0] in self.quote_chars and value[-1] in self.quote_chars):
			value = value[1:-1]

		return KeyValueConfigValue(key, value)

	def format(self, value):
		if self.values_quoted:
			if '"' in value.value:
				return "%s%s'%s'" % (value.key, self.separator, value.value)
			else:
				return '%s%s"%s"' % (value.key, self.separator, value.value)

		else:
			return "%s%s%s" % (value.key, self.separator, value.value)