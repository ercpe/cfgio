# -*- coding: utf-8 -*-

import logging
import os


class ConfigBase(object):

	def __init__(self, filename=None, comment_chars=['#', ';']):
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
			if self.filename and os.path.exists(self.filename):
				with open(self.filename, 'r') as f:
					self._content = [x.rstrip('\n') for x in f.readlines()]
			else:
				self._content = []

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
			v = self.parse(x)
			if v:
				yield v

	def get(self, name, default=None):
		for v in self.read_values():
			if v.key == name:
				return v

		return default

	def find(self, f):
		"""Finds a single configuration value."""

		for i in self.read_values():
			if f(i):
				return i

	def find_all(self, f):
		"""Finds all configuration where f(x) is True"""
		for i in self.read_values():
			if f(i):
				yield i


	def parse(self, s):
		"""Subclasses must implement this method to parse a string into an instance of the configuration value class"""
		pass


class WriteConfig(ReadConfig):

	def __init__(self, *args, **kwargs):
		super(WriteConfig, self).__init__(*args, **kwargs)
		self._pending = []
		self._remove = []

	def set(self, value):
		if value:
			self._pending.append(value)

	def remove(self, key):
		self._remove.append(key)

	def save(self, outfile=None):
		"""Saves the changed values into the underlying file object. Sub-classes can override this method
		to modify the way the values are written to the underlying file object"""

		# make sure that we always read the entire config file before overwriting it.
		list(self.read_values())

		with open(outfile or self.filename, 'w') as o:
			for line in self.content:
				if not line:
					o.write(line + '\n')
					continue

				if self.is_comment(line):
					o.write(line + '\n') # FIXME: Replace commented variable
					continue

				value = self.parse(line)

				if value:
					written = False
					for pending in self._pending:
						if pending.key == value.key:
							o.write(self.format(pending) + '\n')
							self._pending.remove(pending)
							written = True
							break

					if not written:
						for remove_key in self._remove:
							if remove_key == value.key:
								# just pretend that we have written the value
								written = True
								break

					if not written:
						o.write(line + '\n')

				else:
					# pass-through garbage
					o.write(line + '\n')

			for p in self._pending:
				o.write(self.format(p) + '\n')

	def format(self, value):
		"""This method should return a string representing the configuration value in the configuration file format.
		Subclasses must implement this method."""
		pass


class ConfigValueBase(object):
	"""Base class for all ConfigValue classes"""

	def __init__(self, key):
		self._key = key

	@property
	def key(self):
		return self._key

	def __eq__(self, other):
		return isinstance(other, self.__class__) and self.key == other.key