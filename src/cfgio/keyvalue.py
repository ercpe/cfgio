# -*- coding: utf-8 -*-
import logging
from cfgio.base import ReadConfig, ConfigValueBase
import re


class KeyValueConfigValue(ConfigValueBase):

	def __init__(self, *args):
		#print(args)
		self._key, self.value = args

	@property
	def key(self):
		return self._key

	def __repr__(self):
		return "%s=%s" % (self.key, self.value)

	@staticmethod
	def parse(line):
		m = re.match("^(?P<key>.*)\s*=\s*(?P<value>.*)", line, re.IGNORECASE)
		if m:
			return KeyValueConfigValue(*tuple(map(lambda x: x.strip(), m.groups())))
		else:
			raise Exception("Could not parse line: %s" % line)


class KeyValueConfig(ReadConfig):
	value_type = KeyValueConfigValue

	def __init__(self, filename, values_quoted=False):
		super(KeyValueConfig, self).__init__(filename)
		self.values_quoted = values_quoted

	def create_value(self, s):
		x = super(KeyValueConfig, self).create_value(s)
		quote_chars = ['"', "'"]
		if self.values_quoted and x.value and (x.value[0] in quote_chars and x.value[-1] in quote_chars):
			x.value = x.value[1:-1]
		return x