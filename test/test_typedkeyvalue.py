# -*- coding: utf-8 -*-
from cfgio.keyvalue import KeyValueConfigValue
from cfgio.specialized.typedkeyvalue import TypeAwareKeyValueConfig
import os
from test.base import KeyValueConfigTestBase


class TestTypedKVConfig(KeyValueConfigTestBase):

	#def __init__(self):
	#	pass
		#super(TestKeyValueConfigBase, self).__init__(TypeAwareKeyValueConfig, KeyValueConfigValue, 'typekv.cfg')

	@property
	def default_cfg(self):
		return 'typedkv.cfg'

	@property
	def cfg_type(self):
		return TypeAwareKeyValueConfig

	@property
	def cfg_value_type(self):
		return KeyValueConfigValue

	def default_cfg_items(self):
		return [('astring', "This is a string"),
				('anint', 42),
				('afloat', 13.37),
				('abool', True),
				('anotherbool', False),
				('list_of_strings', ["foo", 'bar', "baz"]),
				('another_list', ["foo, bar", 1, 2, 3.4])
				]

	def test_parsing(self):
		cfg = TypeAwareKeyValueConfig(os.path.join(os.path.dirname(__file__), 'typedkv.cfg'))

		for key, valuetype, expected_value in [('astring', str, "This is a string"),
								('anint', int, 42),
								('afloat', float, 13.37),
								('abool', bool, True),
								('anotherbool', bool, False),
								('list_of_strings', list, ["foo", 'bar', "baz"]),
								('another_list', list, ["foo, bar", 1, 2, 3.4])
							]:
			value = cfg.get(key)
			assert value is not None
			assert isinstance(value.value, valuetype)
			assert value.value == expected_value

		l = cfg.get('list_of_strings')
		assert len(l.value) == 3

		for x in l.value:
			assert isinstance(x, str)

		l = cfg.get('another_list')
		assert len(l.value) == 4

		list_types = (str, int, int, float)
		for i, x in enumerate(l.value):
			assert isinstance(x, list_types[i])