# -*- coding: utf-8 -*-

from cfgio.fstab import FstabRWConfig, FstabEntry
import os


class TestFstabConfig(object):

	def test_read(self):
		cfg = FstabRWConfig(os.path.join(os.path.dirname(__file__), 'fstab'))
		assert len(list(cfg.read_values())) == 5

	def test_parse(self):
		cfg = FstabRWConfig(os.path.join(os.path.dirname(__file__), 'fstab'))

		for dev, mp, fs, opts, dump, p in [('/dev/BOOT', '/boot', 'ext2', 'noauto,noatime', '1', '2'),
			('/dev/ROOT', '/', 'ext3', 'noatime', '0', '1'),
			('/dev/SWAP', 'none', 'swap', 'sw', '0', '0'),
			('/dev/cdrom', '/mnt/cdrom', 'auto', 'noauto,ro', '0', '0'),
			('/dev/fd0', '/mnt/floppy', 'auto', 'noauto', '0', '0')]:

			value = cfg.get(dev)
			assert value is not None
			assert value.device == dev
			assert value.mountpoint == mp
			assert value.fs == fs
			assert value.opts == opts
			assert value.dump == dump
			assert value._pass == p


	def test_value_add(self):
		dummy_values = ('/dev/foo', '/mnt/bar', 'none', 'none', '0', '0')

		cfg = FstabRWConfig(os.path.join(os.path.dirname(__file__), 'fstab'))
		cfg.set(dummy_values[0], FstabEntry(dummy_values))
		cfg.save(os.path.join(os.path.dirname(__file__), 'fstab.out'))

		cfg2 = FstabRWConfig(os.path.join(os.path.dirname(__file__), 'fstab.out'))
		v = cfg2.get('/dev/foo')
		assert dummy_values is not None
		assert dummy_values == (v.device, v.mountpoint, v.fs, v.opts, v.dump, v._pass)