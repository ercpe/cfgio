# -*- coding: utf-8 -*-
from abc import abstractmethod, abstractproperty

import os
import tempfile
import pytest
from cfgio.base import ConfigValueBase


class CfgioTestBase(object):

	@abstractproperty
	def default_file(self):
		return None

	@abstractproperty
	def cfg_type(self):
		return None

	@abstractproperty
	def cfg_value_type(self):
		return None

	@abstractproperty
	def default_cfg_items(self):
		return None

	def create_config(self, filename=None, **kwargs):
		f = None

		if not filename:
			filename = self.default_file

		if os.path.isabs(filename):
			f = filename
		else:
			f = os.path.join(os.path.dirname(__file__), filename)

		return self.cfg_type(f, **kwargs)

	def test_empty_config_read(self):
		"""
		Tests that the concrete implementation can be instantiated with an empty or None filename.
		"""
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
		"""
		Tests that the concrete implementation can be instantiated with an empty or None filename.
		Calling save() on the object must result in an exception
		"""
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
		"""
		Tests that the implementation can read values
		"""
		cfg = self.create_config()
		assert len(list(cfg.read_values())) == len(self.default_cfg_items)

		for k, v in self.default_cfg_items:
			x = cfg.get(k)
			assert x is not None
			assert x.value == v

	def test_empty_set(self):
		cfg = self.cfg_type()
		cfg.set(None)
		assert len(cfg._pending) == 0

	def test_find(self):
		cfg = self.create_config()

		x = self.default_cfg_items[0]

		result = cfg.find(lambda v: v.key == x[0])
		assert result is not None
		assert isinstance(result, self.cfg_value_type)
		assert result.value == x[1]

	def test_find_all(self):
		cfg = self.create_config()

		x = self.default_cfg_items[0]
		y = self.default_cfg_items[1]

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

	def test_context_object(self):
		with self.create_config() as cfg:
			assert cfg is not None
			assert isinstance(cfg, self.cfg_type)

		# test autosave
		with pytest.raises(Exception):
			# should raise an exception due to autosave in __exit__
			with self.cfg_type(None) as cfg:
				cfg.set(self.default_cfg_items[0][1])

		# should not raise an exception (autosave only kicks in on clean exit of the with)
		with pytest.raises(ZeroDivisionError):
			with self.cfg_type(None) as cfg:
				cfg.set(self.default_cfg_items[0][1])
				foo = 1 / 0

		# should not raise an exception, due to autosave = False
		with self.cfg_type(None, autosave=False) as cfg:
			cfg.set(self.default_cfg_items[0][1])

		# same here
		with pytest.raises(ZeroDivisionError):
			with self.cfg_type(None, autosave=False) as cfg:
				cfg.set(self.default_cfg_items[0][1])
				foo = 1 / 0

		# should not raise an exception because we didn't change the config
		with self.cfg_type(None) as cfg:
			pass
