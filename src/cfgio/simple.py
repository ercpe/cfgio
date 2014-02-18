# -*- coding: utf-8 -*-

from cfgio.base import ReadConfig, WriteConfig, ConfigValueBase

class KeyOnlyValue(ConfigValueBase):

	def __init__(self, key):
		self.key = key

	@staticmethod
	def parse(line):
		return KeyOnlyValue(line.strip())


class SimpleRWConfig(ReadConfig, WriteConfig):

	value_type = KeyOnlyValue

	def set(self, value):
		self._pending.append(value)

	def save(self, outfile):
		with open(outfile or self.filename, 'w') as f:
			for line in self.content:
				f.write(line + '\n')
