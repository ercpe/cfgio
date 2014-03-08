# -*- coding: utf-8 -*-

import os
import tempfile


class KeyValueConfigTestBase(object):

	@property
	def default_cfg(self):
		return None

	@property
	def cfg_type(self):
		return None

	@property
	def cfg_value_type(self):
		return None

	def default_cfg_items(self):
		return None

	def _create_config(self, filename=None, **kwargs):
		f = None

		if not filename:
			filename = self.default_cfg

		if os.path.isabs(filename):
			f = filename
		else:
			f = os.path.join(os.path.dirname(__file__), filename)

		return self.cfg_type(f, **kwargs)


	def test_read_values(self):
		cfg = self._create_config()
		print(cfg)
		assert len(list(cfg.read_values())) == len(self.default_cfg_items())

		for k, v in self.default_cfg_items():
			x = cfg.get(k)
			assert x is not None
			assert x.value == v

	def test_write(self):
		t = tempfile.mktemp()

		try:
			cfg = self._create_config()
			cfg.set(self.cfg_value_type("aaa", "bbb"))
			cfg.save(t)

			# our new key should by written to the tempfile
			cfg = self._create_config(t)
			assert(len(list(cfg.read_values())) == len(self.default_cfg_items())+1)

			# but not again
			cfg.set(self.cfg_value_type("aaa", "bbb"))
			cfg.save(t)
			cfg = self._create_config(t)
			assert(len(list(cfg.read_values())) == len(self.default_cfg_items())+1)

		finally:
			if os.path.exists(t):
				os.remove(t)
