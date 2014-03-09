# -*- coding: utf-8 -*-
import tempfile
import pytest

from cfgio.fstab import FstabConfig, FstabEntry
import os
from test.base import CfgioTestBase


class TestFstabConfig(CfgioTestBase):

	@property
	def default_file(self):
		return 'fstab'

	@property
	def cfg_type(self):
		return FstabConfig

	@property
	def cfg_value_type(self):
		return FstabEntry

	@property
	def default_cfg_items(self):
		return [
			('/dev/BOOT', FstabEntry('/dev/BOOT', '/boot', 'ext2', 'noauto,noatime', '1', '2')),
			('/dev/ROOT', FstabEntry('/dev/ROOT', '/', 'ext3', 'noatime', '0', '1')),
			('/dev/SWAP', FstabEntry('/dev/SWAP', 'none', 'swap', 'sw', '0', '0')),
			('/dev/cdrom', FstabEntry('/dev/cdrom', '/mnt/cdrom', 'auto', 'noauto,ro', '0', '0')),
			('/dev/fd0', FstabEntry('/dev/fd0', '/mnt/floppy', 'auto', 'noauto', '0', '0'))
		]

	def test_instantiate_fstabentry(self):
		with pytest.raises(Exception):
			for x in range(1, 5):
				FstabEntry(tuple(['' * x]))

	def test_parse_FIXME(self):
		cfg = FstabConfig(os.path.join(os.path.dirname(__file__), 'fstab'))

		for dev, mp, fs, opts, dump, p in [('/dev/BOOT', '/boot', 'ext2', 'noauto,noatime', '1', '2'),
			('/dev/ROOT', '/', 'ext3', 'noatime', '0', '1'),
			('/dev/SWAP', 'none', 'swap', 'sw', '0', '0'),
			('/dev/cdrom', '/mnt/cdrom', 'auto', 'noauto,ro', '0', '0'),
			('/dev/fd0', '/mnt/floppy', 'auto', 'noauto', '0', '0')]:

			value = cfg.get(dev)
			assert value is not None
			assert value.device == dev
			assert value.mountpoint == mp
			assert value.filesystem == fs
			assert value.opts == opts
			assert value.dump == dump
			assert value._pass == p


	def test_value_add(self):
		t = tempfile.mktemp()

		try:
			dummy_values = ('/dev/foo', '/mnt/bar', 'none', 'none', '0', '0')

			cfg = FstabConfig(os.path.join(os.path.dirname(__file__), 'fstab'))
			cfg.set(FstabEntry(*dummy_values))
			cfg.save(t)

			cfg2 = FstabConfig(t)
			v = cfg2.get('/dev/foo')
			assert v is not None
			assert dummy_values == (v.device, v.mountpoint, v.filesystem, v.opts, v.dump, v._pass)

		finally:
			if os.path.exists(t):
				os.remove(t)

	def test_delete(self):
		t = tempfile.mktemp()

		try:
			cfg = FstabConfig(os.path.join(os.path.dirname(__file__), 'fstab'))
			cfg.remove('/dev/ROOT')
			cfg.save(t)

			cfg2 = FstabConfig(t)
			assert cfg2.get('/dev/ROOT') is None

		finally:
			if os.path.exists(t):
				os.remove(t)

	def test_delete_set_precedence(self):
		"""Tests that a call to .set() takes precendence over a call to .remove() with the same key"""

		t = tempfile.mktemp()

		try:
			cfg = FstabConfig(os.path.join(os.path.dirname(__file__), 'fstab'))
			cfg.remove('/dev/ROOT')
			cfg.set(FstabEntry('/dev/ROOT', '/', 'ext4', 'defaults', 0, 2))
			cfg.save(t)

			cfg2 = FstabConfig(t)
			assert cfg2.get('/dev/ROOT') is not None

		finally:
			if os.path.exists(t):
				os.remove(t)