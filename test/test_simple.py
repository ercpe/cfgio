# -*- coding: utf-8 -*-

from cfgio.simple import SimpleConfig, KeyOnlyValue
import os
import tempfile
from test.base import CfgioTestBase


class TestSimpleConfig(CfgioTestBase):

	@property
	def default_file(self):
		return 'simple'

	@property
	def cfg_type(self):
		return SimpleConfig

	@property
	def cfg_value_type(self):
		return KeyOnlyValue

	@property
	def default_cfg_items(self):
		return [
			'foo',
			'bar',
			'baz',
			'bat',
		]

	def test_read_values(self):
		"""
		Tests that the implementation can read values
		"""
		cfg = self.create_config()
		assert len(list(cfg.read_values())) == len(self.default_cfg_items)

		for k in self.default_cfg_items:
			x = cfg.get(k)
			assert x is not None
			assert x.key == k


	def test_find(self):
		cfg = self.create_config()

		x = self.default_cfg_items[0]

		result = cfg.find(lambda v: v.key == x)
		assert result is not None
		assert isinstance(result, self.cfg_value_type)
		assert result.key == x

	def test_find_all(self):
		cfg = self.create_config()

		expected_items = [
			self.default_cfg_items[0],
			self.default_cfg_items[1]
		]

		result = list(cfg.find_all(lambda v: v.key in expected_items))
		assert result is not None
		assert len(result) == 2

		for item in result:
			assert isinstance(item, self.cfg_value_type)
			assert item.key in expected_items

	def test_write(self):
		t = tempfile.mktemp()

		try:
			cfg = self.create_config()
			cfg.set(KeyOnlyValue("blah"))
			cfg.save(t)

			# our new key should by written to the tempfile
			cfg = self.create_config(t)
			assert(len(list(cfg.read_values())) == 5)

			# but not again
			cfg.set(KeyOnlyValue("blah"))
			cfg.save(t)
			cfg = self.create_config(t)
			assert(len(list(cfg.read_values())) == 5)

		finally:
			if os.path.exists(t):
				os.remove(t)