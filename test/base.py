# -*- coding: utf-8 -*-

import os
import tempfile
import pytest
from cfgio.base import ConfigValueBase


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

	def test_empty_config_read(self):
		# TODO: Move to common base class for tests (see test_base.py)
		try:
			self.cfg_type()
		except Exception as ex:
			pytest.fail("Failed to instantiate a config class without filename (caught: %s)" % ex)

		try:
			for filename in [None, '']:
				cfg = self.cfg_type(filename)
				assert len(list(cfg.read_values())) == 0
		except Exception as ex:
			pytest.fail("Failed to instantiate config class with filename=%s (caught: %s)" % (filename, ex))

	def test_empty_config_write(self):
		# TODO: Move to common base class for tests (see test_base.py)
		try:
			cfg = self.cfg_type()
		except Exception as ex:
			pytest.fail("Failed to instantiate config class without filename (caught: %s)" % ex)

		cfg.set('foo')
		with pytest.raises(Exception):
			cfg.save()

		try:
			for filename in [None, '']:
				cfg = self.cfg_type(filename)
				assert len(list(cfg.read_values())) == 0

				cfg.set('foo')
				with pytest.raises(Exception):
					cfg.save()

		except Exception as ex:
			pytest.fail("Failed to instantiate config class with filename=%s (caught: %s)" % (filename, ex))

	def test_read_values(self):
		cfg = self._create_config()
		print(cfg)
		assert len(list(cfg.read_values())) == len(self.default_cfg_items())

		for k, v in self.default_cfg_items():
			x = cfg.get(k)
			assert x is not None
			assert x.value == v

	def test_set(self):
		t = tempfile.mktemp()

		try:
			cfg = self._create_config()
			cfg.set(None)
			assert len(cfg._pending) == 0
			cfg.save(t)
		except Exception as ex:
			pytest.fail("Caught %s when set()ing None" % ex)
		finally:
			if os.path.exists(t):
				os.remove(t)

	def test_set_kv(self):
		cfg = self._create_config()
		cfg.set('some-key', 'some-value')
		assert len(cfg._pending) == 1

		with pytest.raises(Exception):
			cfg = self._create_config()
			cfg.set('foo', 'bar', 'baz')


	def test_write(self):
		t = tempfile.mktemp()

		try:
			cfg = self._create_config()
			cfg.set(self.cfg_value_type("aaa", "bbb"))
			cfg.save(t)

			# our new key should by written to the tempfile
			cfg = self._create_config(t)
			print(list(cfg.read_values()))

			assert(len(list(cfg.read_values())) == len(self.default_cfg_items())+1)

			# but not again
			cfg.set(self.cfg_value_type("aaa", "bbb"))
			cfg.save(t)
			cfg = self._create_config(t)
			assert(len(list(cfg.read_values())) == len(self.default_cfg_items())+1)

		finally:
			if os.path.exists(t):
				os.remove(t)

	def test_find(self):
		cfg = self._create_config()

		x = self.default_cfg_items()[0]

		result = cfg.find(lambda v: v.key == x[0])
		assert result is not None
		assert isinstance(result, self.cfg_value_type)
		assert result.value == x[1]

	def test_find_all(self):
		cfg = self._create_config()

		x = self.default_cfg_items()[0]
		y = self.default_cfg_items()[1]

		expected_items = {
			x[0]: x[1],
			y[0]: y[1],
		}

		result = list(cfg.find_all(lambda v: v.key in [x[0], y[0]]))
		assert result is not None
		assert len(result) == 2

		for item in result:
			assert isinstance(item, self.cfg_value_type)
			assert item.key in expected_items
			assert item.value == expected_items[item.key]


	def test_config_value_equals(self):
		option1 = ConfigValueBase('foo')
		option2 = ConfigValueBase('foo')

		assert option1 == option2
		assert option1 != "foo"