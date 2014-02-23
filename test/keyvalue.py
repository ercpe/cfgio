# -*- coding: utf-8 -*-

import os
from cfgio.keyvalue import KeyValueConfig

class TestKeyValueConfig(object):

	def _build_cfg(self, **kwargs):
		return KeyValueConfig(os.path.join(os.path.dirname(__file__), 'keyvalue.cfg'), **kwargs)

	def test_read(self):
		cfg = self._build_cfg()
		assert len(list(cfg.read_values())) == 6

	def test_read_values(self):
		cfg = self._build_cfg()

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
		cfg = self._build_cfg(values_quoted=True)

		x = cfg.get('with_quotes')
		assert x is not None
		assert x.value == "yeah"
