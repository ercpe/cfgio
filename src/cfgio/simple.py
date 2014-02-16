# -*- coding: utf-8 -*-

from cfgio.base import ReadConfig, WriteConfig

class SimpleRWConfig(ReadConfig, WriteConfig):

	def get(self, name, default=None):
		for x in self.cleaned():
			if name == x:
				return x

		return default


	def set(self, value):
		values = None
		if isinstance(value, (list, tuple)):
			values = value
		else:
			values = [value]

		for x in value:
			if not x in self.cleaned():
				self._pending.append(x)


	def save(self):
		with open(self.filename, 'a') as f:
			for x in self._pending:
				f.write(x)
