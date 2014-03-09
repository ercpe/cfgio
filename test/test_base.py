# -*- coding: utf-8 -*-
import pytest
from cfgio.base import ReadConfig, WriteConfig


class TestBaseClasses(object):

	def test_empty_config_read(self):
		try:
			ReadConfig()
		except Exception as ex:
			pytest.fail("Failed to instantiate a ReadConfig without filename (caught: %s)" % ex)

		try:
			for filename in [None, '']:
				cfg = ReadConfig(filename)
				assert len(list(cfg.read_values())) == 0
		except Exception as ex:
			pytest.fail("Failed to instantiate a ReadConfig with filename=%s (caught: %s)" % (filename, ex))

	def test_empty_config_write(self):
		try:
			cfg = WriteConfig()
		except Exception as ex:
			pytest.fail("Failed to instantiate a ReadConfig without filename (caught: %s)" % ex)

		cfg.set('foo')
		with pytest.raises(Exception):
			cfg.save()

		try:
			for filename in [None, '']:
				cfg = WriteConfig(filename)
				assert len(list(cfg.read_values())) == 0

				cfg.set('foo')
				with pytest.raises(Exception):
					cfg.save()

		except Exception as ex:
			pytest.fail("Failed to instantiate a ReadConfig with filename=%s (caught: %s)" % (filename, ex))
