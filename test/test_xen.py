# -*- coding: utf-8 -*-
import os
import tempfile
import pytest
from cfgio.keyvalue import KeyValueConfigValue
from cfgio.specialized.xen import XenConfig, XenDomUDiskConfigValue
from test.base import KeyValueConfigTestBase


class TestTypedKVConfig(KeyValueConfigTestBase):

	@property
	def default_cfg(self):
		return 'xen.cfg'

	@property
	def cfg_type(self):
		return XenConfig

	@property
	def cfg_value_type(self):
		return KeyValueConfigValue

	def default_cfg_items(self):
		return [
			('kernel', "/boot/vm-kernel"),
			('vcpus', 4),
			('memory', 1024),
			('name', "test-domu"),
			('disk', [
				XenDomUDiskConfigValue('phy', '/dev/foo/bar-hdd0', '/dev/xvda1', 'r'),
				XenDomUDiskConfigValue('file', '/tmp/bar-hdd1', '/dev/xvda2', 'w'),
			]),
			('root', "/dev/xvda1"),
			('vif', [ 'mac=00:11:22:33:44:55,bridge=br0', ])
		]


	def test_config_value_properties(self):
		x = XenDomUDiskConfigValue('phy', '/dev/foo/bar-hdd0', '/dev/xvda1', 'r')
		assert x.is_readonly
		assert not x.is_readwrite

		x = XenDomUDiskConfigValue('file', '/tmp/bar-hdd1', '/dev/xvda2', 'w')
		assert not x.is_readonly
		assert x.is_readwrite

	def test_parse_list(self):
		cfg = self.cfg_type()
		cfg.parse_list('foo', None)

	def test_parse_disk(self):
		cfg = self._create_config()

		disks = cfg.get('disk')

		assert disks is not None
		assert isinstance(disks.value, list)
		assert len(disks.value) == 2

		for i, values in enumerate([
				('phy', '/dev/foo/bar-hdd0', '/dev/xvda1', 'r'),
				('file', '/tmp/bar-hdd1', '/dev/xvda2', 'w'),
			]):

			assert isinstance(disks.value[i], XenDomUDiskConfigValue)
			assert (disks.value[i].backend_access, disks.value[i].backend, disks.value[i].frontend, disks.value[i].mode) == \
						values

	def test_write_disk(self):
		t = tempfile.mktemp()

		try:
			cfg = self.cfg_type()

			d = XenDomUDiskConfigValue('phy', '/dev/foo/bar-hdd0', '/dev/xvda1', 'r')

			cfg.set(KeyValueConfigValue('disk', [d]))
			cfg.save(t)

			cfg = self._create_config(t)

			disks = cfg.get('disk')
			assert disks is not None
			assert isinstance(disks.value, list)
			assert len(disks.value) == 1
			assert isinstance(disks.value[0], XenDomUDiskConfigValue)

			assert (disks.value[0].backend_access, disks.value[0].backend, disks.value[0].frontend, disks.value[0].mode) == \
						('phy', '/dev/foo/bar-hdd0', '/dev/xvda1', 'r')


		finally:
			if os.path.exists(t):
				os.remove(t)