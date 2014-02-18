# -*- coding: utf-8 -*-

from cfgio.base import ReadConfig, WriteConfig, ConfigValueBase
import re

class FstabEntry(ConfigValueBase):
	"""
	Represents a single entry in the /etc/fstab format.
	"""

	line_re = re.compile(r"^\s*(?P<dev>[^\s]+)\s+(?P<mountpoint>[^\s]+)\s+(?P<fs>[\w\d]+)\s+(?P<opts>[^\s]+)\s+(?P<dump>\d+)\s+(?P<pass>\d+)\s*", re.IGNORECASE)

	def __init__(self, *args):
		if len(*args) != 6:
			raise Exception("Need a 6 items argument!")

		self.device, self.mountpoint, self.fs, self.opts, self.dump, self._pass = tuple(*args)
		self._device, self._mountpoint, self._fs, self._opts, self._dump, self.__pass = tuple(*args)

	@property
	def key(self):
		return self.device

	@staticmethod
	def parse(line):
		m = FstabEntry.line_re.match(line)
		return FstabEntry(m.groups())

	def __repr__(self):
		return "%s on %s (%s), opts: %s (%s/%s)" % (self.device, self.mountpoint, self.fs, self.opts, self.dump, self._pass)


class FstabConfig(ReadConfig, WriteConfig):
	"""
	Read/Write implementation of the /etc/fstab (or mtab) file format. Uses the FstabEntry class to represent
	entries.
	"""

	value_type = FstabEntry

	def set(self, name, value):
		self._pending.append(value)

	def _format(self, value):
		return '{}\t{}\t{}\t{}\t{}\t{}'.format(value.device, value.mountpoint, value.fs, value.opts, value.dump, value._pass)

	def save(self, outfile):
		with open(outfile or self.filename, 'w') as f:
			for line in self.content:
				if line and not self.is_comment(line):
					m = FstabEntry.line_re.match(line)
					written = False
					for value in self._pending:
						if m and m.group('dev') == value._device:
							f.write(self._format(value) + '\n')
							self._pending.remove(value)
							written = True
							break

					if not written:
						f.write(line + '\n')
				else:
					f.write(line + '\n')

			for value in self._pending:
				f.write(self._format(value) + '\n')
