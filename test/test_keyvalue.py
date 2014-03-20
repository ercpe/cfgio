# -*- coding: utf-8 -*-

import os
import tempfile
import pytest
from cfgio.keyvalue import KeyValueConfig, KeyValueConfigValue
from test.base import CfgioTestBase


class TestKeyValueConfig(CfgioTestBase):

	@property
	def default_file(self):
		return 'keyvalue.cfg'

	@property
	def cfg_type(self):
		return KeyValueConfig

	@property
	def cfg_value_type(self):
		return KeyValueConfigValue

	@property
	def default_cfg_items(self):
		return [('test', 'blah'),
				('foo', 'bar'),
				('baz', ''),
				('the_answer', '42'),
				('inline_comments', 'yes # or no?'),
				('with_quotes', '"yeah"')
				]

	def test_set_kv(self):
		cfg = self.create_config()
		cfg.set('some-key', 'some-value')
		assert len(cfg._pending) == 1

		with pytest.raises(Exception):
			cfg = self.create_config()
			cfg.set('foo', 'bar', 'baz')

	def test_write(self):
		t = tempfile.mktemp()

		try:
			cfg = self.create_config()
			cfg.set(self.cfg_value_type("aaa", "bbb"))
			cfg.save(t)

			# our new key should by written to the tempfile
			cfg = self.create_config(t)
			print(list(cfg.read_values()))

			assert(len(list(cfg.read_values())) == len(self.default_cfg_items)+1)

			# but not again
			cfg.set(self.cfg_value_type("aaa", "bbb"))
			cfg.save(t)
			cfg = self.create_config(t)
			assert(len(list(cfg.read_values())) == len(self.default_cfg_items)+1)

		finally:
			if os.path.exists(t):
				os.remove(t)

	def test_read_values_with_space_separator(self):
		cfg = self.create_config('keyvalue_space.cfg', separator=" ", values_quoted=False)

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
		cfg = self.create_config(values_quoted=True)

		x = cfg.get('with_quotes')
		assert x is not None
		assert x.value == "yeah"

	def test_read_quoted_values_with_space_separator(self):
		cfg = self.create_config('keyvalue_space.cfg', separator=" ", values_quoted=True)

		x = cfg.get('with_quotes')
		assert x is not None
		assert x.value == "yeah"

	def test_write_space_separator(self):
		t = tempfile.mktemp()

		try:
			cfg = self.create_config('keyvalue_space.cfg', separator=" ")
			cfg.set(KeyValueConfigValue("aaa", "bbb"))
			cfg.save(t)

			# our new key should by written to the tempfile
			cfg = self.create_config(t, separator=" ")
			assert(len(list(cfg.read_values())) == 5)

			# but not again
			cfg.set(KeyValueConfigValue("aaa", "bbb"))
			cfg.save(t)
			cfg = self.create_config(t, separator=" ")
			assert(len(list(cfg.read_values())) == 5)


			cfg = self.create_config(t, values_quoted=True, separator=" ")
			assert len(list(cfg.read_values())) == 5
			v = cfg.get('aaa')
			assert v is not None
			assert v.value == "bbb"

			# but not again
			cfg.set(KeyValueConfigValue("aaa", "bbb"))
			cfg.save(t)
			cfg = self.create_config(t, separator=" ")
			assert(len(list(cfg.read_values())) == 5)
		finally:
			if os.path.exists(t):
				os.remove(t)

	def test_parse_garbage(self):
		cfg = self.create_config(None, separator="=")

		assert cfg.parse("foobar") is None

	def test_uncomment(self):
		t = tempfile.mktemp()

		try:
			def _inspect_file(file):
				no_comments = 0
				no_values = 0
				with open(file, 'r') as f:
					for line in [x.strip() for x in f.readlines()]:
						if not line:
							continue

						if line.startswith("#"):
							no_comments += 1
						else:
							no_values += 1
				return no_comments, no_values


			orig_comments, orig_values = _inspect_file(os.path.join(os.path.dirname(__file__), self.default_file))

			cfg = self.create_config()
			cfg.set('inactive_value', 0)

			cfg.save(t)

			written_comments, written_values = _inspect_file(t)

			assert written_comments == orig_comments -1
			assert written_values == orig_values +1
		finally:
			if os.path.exists(t):
				os.remove(t)