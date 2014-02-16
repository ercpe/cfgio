# -*- coding: utf-8 -*-

import logging


class ConfigBase(object):

	def __init__(self, filename, comment_chars=['#', ';']):
		self.filename = filename
		self._content = None
		self.comment_chars = comment_chars

	@property
	def content(self):
		if not self._content:
			with open(self.filename, 'r') as f:
				self._content = [x.rstrip('\n') for x in f.readlines()]

		return self._content

	@property
	def cleaned(self):
		for line in self.content:
			if line.strip() and not self.is_comment(line):
				yield line

	def is_comment(self, line):
		return line[0] in self.comment_chars


class ReadConfig(ConfigBase):

	def read_values(self):
		for x in self.cleaned:
			yield self.value_type.parse(x)

	def get(self, name, default=None):
		for v in self.read_values():
			if v.key == name:
				return v

		return default


class WriteConfig(ConfigBase):

	def __init__(self, *args, **kwargs):
		super(WriteConfig, self).__init__(*args, **kwargs)
		self._pending = []

	def set(self, name, value):
		pass

	def save(self, outfile):
		"""Saves the changed values into the underlying file object"""
		pass


class ConfigValueBase(object):

	@staticmethod
	def parse(line):
		pass

	@property
	def key(self):
		pass