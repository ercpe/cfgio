# -*- coding: utf-8 -*-

import os
import tempfile
from cfgio.keyvalue import KeyValueConfig, KeyValueConfigValue


class TestKeyValueConfig(object):

	def _create_config(self, filename=None, **kwargs):
		return KeyValueConfig(filename or os.path.join(os.path.dirname(__file__), 'keyvalue.cfg'), **kwargs)

	def test_read(self):
		cfg = self._create_config()
		assert len(list(cfg.read_values())) == 6

	def test_read_values(self):
		cfg = self._create_config()

		for k, v in [
						('test', 'blah'),
						('foo', 'bar'),
						('baz', ''),
						('the_answer', '42'),
						('inline_comments', 'yes # or no?'),
						('with_quotes', '"yeah"')
					]:
			x = cfg.get(k)
			assert x is not None
			assert x.value == v

	def test_quoted_values(self):
		cfg = self._create_config(values_quoted=True)

		x = cfg.get('with_quotes')
		assert x is not None
		assert x.value == "yeah"


	def test_write(self):
		t = tempfile.mktemp()

		try:
			cfg = self._create_config()
			cfg.set(KeyValueConfigValue("aaa", "bbb"))
			cfg.save(t)

			# our new key should by written to the tempfile
			cfg = self._create_config(t)
			assert(len(list(cfg.read_values())) == 7)

			# but not again
			cfg.set(KeyValueConfigValue("aaa", "bbb"))
			cfg.save(t)
			cfg = self._create_config(t)
			assert(len(list(cfg.read_values())) == 7)


			cfg = self._create_config(t, values_quoted=True)
			assert len(list(cfg.read_values())) == 7
			v = cfg.get('aaa')
			assert v is not None
			assert v.value == "bbb"

			# but not again
			cfg.set(KeyValueConfigValue("aaa", "bbb"))
			cfg.save(t)
			cfg = self._create_config(t)
			assert(len(list(cfg.read_values())) == 7)

		finally:
			if os.path.exists(t):
				os.remove(t)
