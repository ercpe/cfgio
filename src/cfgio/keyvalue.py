# -*- coding: utf-8 -*-
import logging
from cfgio.base import ReadConfig, ConfigValueBase, WriteConfig
import re


class KeyValueConfigValue(ConfigValueBase):

	def __init__(self, *args):
		super(KeyValueConfigValue, self).__init__(args[0])
		self.value = args[1]

	def __repr__(self):
		return "%s=%s" % (self.key, self.value)


class KeyValueConfig(WriteConfig):
	"""Key-Value configuration file format. Key-value pairs are store line by line. Values may be quoted"""

	quote_chars = ['"', "'"]

	def __init__(self, filename, values_quoted=False):
		super(KeyValueConfig, self).__init__(filename)
		self.values_quoted = values_quoted

	def parse(self, line):
		m = re.match("^(?P<key>.*)\s*=\s*(?P<value>.*)", line, re.IGNORECASE)
		if not m:
			raise Exception("Could not parse line: %s" % line)

		x = KeyValueConfigValue(*tuple(map(lambda x: x.strip(), m.groups())))

		if self.values_quoted and x.value and (x.value[0] in self.quote_chars and x.value[-1] in self.quote_chars):
			x.value = x.value[1:-1]

		return x

	def format(self, value):
		pass