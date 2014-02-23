# -*- coding: utf-8 -*-

import logging


class ConfigBase(object):

	def __init__(self, filename, comment_chars=['#', ';']):
		"""
		:string filename: The filename of the file to read from.
		:list comment_chars: A list of characters to recognize comments in the file
		"""
		self.filename = filename
		self._content = None
		self.comment_chars = comment_chars

	@property
	def content(self):
		"""
		Reads the file and returns a list of strings.
		:return: A list of strings
		"""
		if not self._content:
			with open(self.filename, 'r') as f:
				self._content = [x.rstrip('\n') for x in f.readlines()]

		return self._content

	@property
	def cleaned(self):
		"""
		Takes the content of the file from self.content and yields only non-empty, non-comment
		lines.
		"""
		for line in self.content:
			if line.strip() and not self.is_comment(line):
				yield line

	def is_comment(self, line):
		return line[0] in self.comment_chars


class ReadConfig(ConfigBase):

	def read_values(self):
		for x in self.cleaned:
			yield self.create_value(x)

	def create_value(self, s):
		return self.value_type.parse(s)

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
		"""Saves the changed values into the underlying file object. Sub-classes must implement this method
		to actually save the values to the file"""
		pass


class ConfigValueBase(object):
	"""Base class for all ConfigValue classes"""

	@staticmethod
	def parse(line):
		pass

	@property
	def key(self):
		pass

	def __eq__(self, other):
		return isinstance(other, self.__class__) and self.key == other.key