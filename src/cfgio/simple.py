# -*- coding: utf-8 -*-

from cfgio.base import ReadConfig, WriteConfig, ConfigValueBase

class KeyOnlyValue(ConfigValueBase):

	def __init__(self, key):
		self._key = key

	@staticmethod
	def parse(line):
		return KeyOnlyValue(line.strip())

	@property
	def key(self):
		return self._key


class SimpleConfig(ReadConfig, WriteConfig):

	value_type = KeyOnlyValue

	def set(self, value):
		self._pending.append(value)

	def save(self, outfile):
		with open(outfile or self.filename, 'w') as f:
			for line in self.content:
				f.write(line + '\n')

			for p in self._pending:
				if not p in list(self.read_values()):
					f.write("%s\n" % p.key)
