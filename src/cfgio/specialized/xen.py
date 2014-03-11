# -*- coding: utf-8 -*-
from cfgio.base import ConfigValueBase
from cfgio.specialized.typedkeyvalue import TypeAwareKeyValueConfig


class XenDomUDiskConfigValue(ConfigValueBase):

	def __init__(self, backend_access, backend, frontend, mode):
		"""
		Creates a new instance of the XenDomUDiskConfigValue
		:param backend_access:The backend access to the underlying storage (should by something like 'phy' for physical
		 		disks or 'file' for file-based loopback backends.
		:param backend: The backend object. May be a path (like /foo/bar) or a hex value
		:param frontend: The frontend device. May be a device name (like sda1) or a hex value
		:param mode: The access mode ('r' for read-only, 'w' for read/write)
		"""
		super(XenDomUDiskConfigValue, self).__init__(frontend)
		self.backend_access = backend_access
		self.backend = backend
		self.frontend = frontend
		self.mode = mode

	@property
	def is_readonly(self):
		return self.mode == "r"

	@property
	def is_readwrite(self):
		return self.mode == "w"


class XenDomUVifConfigValue(ConfigValueBase):

	def __init__(self, **kwargs):
		self.mac = kwargs.get('mac')
		self.bridge = kwargs.get('bridge')
		super(XenDomUVifConfigValue, self).__init__(self.mac)


class XenConfig(TypeAwareKeyValueConfig):

	def parse_list(self, key, value):
		l = super(XenConfig, self).parse_list(key, value)

		if not l:
			return l

		if key == "vif":
			return [self.parse_vif_stanza(x) for x in l]

		if key == "disk":
			return [self.parse_disk_stanza(x) for x in l]

		return l

	def parse_disk_stanza(self, stanza):
		"""
		Parses a disk stanze into a XenDomUDiskConfigValue. The man page describes the stanza format as:


		Each stanza has 3 terms, separated by commas, "backend-dev,frontend-dev,mode".
		backend-dev
		The device in the backend domain that will be exported to the guest (frontend) domain. Supported formats include:
		phy:device - export the physical device listed. The device can be in symbolic form, as in sda7, or as the hex major/minor number, as in 0x301 (which is hda1).

		file://path/to/file - export the file listed as a loopback device. This will take care of the loopback setup before exporting the device.

		frontend-dev
		How the device should appear in the guest domain. The device can be in symbolic form, as in sda7, or as the hex major/minor number, as in 0x301 (which is hda1).
		mode
		The access mode for the device. There are currently 2 valid options, r (read-only), w (read/write).

		:param stanza: A stanza string to parse
		"""

		backend, frontend, mode = tuple(stanza.split(','))

		backend_access = None
		if ':' in backend:
			backend_access = backend[:backend.index(':')]

		backend_path = backend[len(backend_access)+1:]
		if backend_access == "file":
			backend_path = backend_path[1:]

		return XenDomUDiskConfigValue(backend_access, backend_path, frontend, mode)

	def parse_vif_stanza(self, stanza):
		"""
		Parses a vif stanza into a XenDomUVifConfigValue. The man page describes the format as:

		Each stanza specifies a set of name = value options separated by commas, in the form: "name1=value1, name2=value2, ..."

		:param stanza: The string to parse
		"""

		chunks = [x.strip() for x in stanza.split(",")]

		d = {}
		for x in chunks:
			y = self.parse(x)
			d[y.key] = y.value

		return XenDomUVifConfigValue(**d)

	def format_value(self, value):
		if isinstance(value, XenDomUDiskConfigValue):
			return "'%s:%s%s,%s,%s'" % (
				value.backend_access,
				"/" if value.backend_access == "file" else "",
				value.backend,
				value.frontend,
				value.mode
			)

		if isinstance(value, XenDomUVifConfigValue):
			return "'mac=%s,bridge=%s'" % (value.mac, value.bridge)

		return super(XenConfig, self).format_value(value)