# -*- coding: utf-8 -*-

from cfgio.simple import SimpleConfig, KeyOnlyValue
import os
import tempfile

class TestSimpleConfig(object):

	def _create_config(self, filename=None):
		return SimpleConfig(filename or os.path.join(os.path.dirname(__file__), 'simple'))

	def test_read(self):
		cfg = self._create_config()
		assert len(list(cfg.read_values())) == 4

	def test_read_values(self):
		values = self._create_config().read_values()

		for v in values:
			assert isinstance(v, KeyOnlyValue)
			assert v.key in ['foo', 'bar', 'baz', 'bat']

	def test_write(self):
		t = tempfile.mktemp()

		try:
			cfg = self._create_config()
			cfg.set(KeyOnlyValue("blah"))
			cfg.save(t)

			# our new key should by written to the tempfile
			cfg = self._create_config(t)
			assert(len(list(cfg.read_values())) == 5)

			# but not again
			cfg.set(KeyOnlyValue("blah"))
			cfg.save(t)
			cfg = self._create_config(t)
			assert(len(list(cfg.read_values())) == 5)

		finally:
			os.remove(t)