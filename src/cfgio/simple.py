# -*- coding: utf-8 -*-

from cfgio.base import ReadConfig, WriteConfig, ConfigValueBase


class KeyOnlyValue(ConfigValueBase):
	pass


class SimpleConfig(WriteConfig):
	"""Simple configuration file format. This file format contains one key or "statement" per line."""

	def parse(self, s):
		return KeyOnlyValue(s.strip())

	def format(self, value):
		return value.key