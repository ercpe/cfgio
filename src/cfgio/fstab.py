# -*- coding: utf-8 -*-

from cfgio.base import ReadConfig, WriteConfig, ConfigValueBase
import re


class FstabEntry(ConfigValueBase):
	"""
	Represents a single entry in the /etc/fstab format.
	"""

	def __init__(self, *args):
		if len(args) != 6:
			raise Exception("Need a 6 items argument!")

		super(FstabEntry, self).__init__(args[0])

		self.device, self.mountpoint, self.filesystem, self.opts, self.dump, self._pass = args
		self._device, self._mountpoint, self._filesystem, self._opts, self._dump, self.__pass = args

	@property
	def value(self):
		# compatibility for other KeyValueConfigs
		return self


class FstabConfig(WriteConfig):
	"""
	Read/Write implementation of the /etc/fstab (or mtab) file format. Uses the FstabEntry class to represent
	entries.
	"""

	line_re = re.compile(r"^\s*(?P<dev>[^\s]+)\s+(?P<mountpoint>[^\s]+)\s+(?P<fs>[\w\d]+)\s+(?P<opts>[^\s]+)\s+(?P<dump>\d+)\s+(?P<pass>\d+)\s*", re.IGNORECASE)

	def parse(self, s):
		m = self.line_re.match(s)
		if m:
			return FstabEntry(*m.groups())
		return None

	def format(self, value):
		return '{}\t{}\t{}\t{}\t{}\t{}'.format(value.device, value.mountpoint, value.filesystem, value.opts, value.dump, value._pass)