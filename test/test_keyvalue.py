# -*- coding: utf-8 -*-

import os
import tempfile
from cfgio.keyvalue import KeyValueConfig, KeyValueConfigValue
from test.base import KeyValueConfigTestBase


class TestKeyValueConfig(KeyValueConfigTestBase):

	@property
	def default_cfg(self):
		return 'keyvalue.cfg'

	@property
	def cfg_type(self):
		return KeyValueConfig

	@property
	def cfg_value_type(self):
		return KeyValueConfigValue

	def default_cfg_items(self):
		return [('test', 'blah'),
				('foo', 'bar'),
				('baz', ''),
				('the_answer', '42'),
				('inline_comments', 'yes # or no?'),
				('with_quotes', '"yeah"')
				]

	def test_read_values_with_space_separator(self):
		cfg = self._create_config('keyvalue_space.cfg', separator=" ")

		for k, v in [
						('test', 'blah'),
						('foo', 'bar'),
						('inline_comments', 'yes # or no?'),
						('with_quotes', '"yeah"')
					]:
			x = cfg.get(k)
			assert x is not None
			assert x.value == v

	def test_read_quoted_values(self):
		cfg = self._create_config(values_quoted=True)

		x = cfg.get('with_quotes')
		assert x is not None
		assert x.value == "yeah"

	def test_read_quoted_values_with_space_separator(self):
		cfg = self._create_config('keyvalue_space.cfg', separator=" ", values_quoted=True)

		x = cfg.get('with_quotes')
		assert x is not None
		assert x.value == "yeah"

	def test_write_space_separator(self):
		t = tempfile.mktemp()

		try:
			cfg = self._create_config('keyvalue_space.cfg', separator=" ")
			cfg.set(KeyValueConfigValue("aaa", "bbb"))
			cfg.save(t)

			# our new key should by written to the tempfile
			cfg = self._create_config(t, separator=" ")
			assert(len(list(cfg.read_values())) == 5)

			# but not again
			cfg.set(KeyValueConfigValue("aaa", "bbb"))
			cfg.save(t)
			cfg = self._create_config(t, separator=" ")
			assert(len(list(cfg.read_values())) == 5)


			cfg = self._create_config(t, values_quoted=True, separator=" ")
			assert len(list(cfg.read_values())) == 5
			v = cfg.get('aaa')
			assert v is not None
			assert v.value == "bbb"

			# but not again
			cfg.set(KeyValueConfigValue("aaa", "bbb"))
			cfg.save(t)
			cfg = self._create_config(t, separator=" ")
			assert(len(list(cfg.read_values())) == 5)
		finally:
			if os.path.exists(t):
				os.remove(t)
