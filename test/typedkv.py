# -*- coding: utf-8 -*-
from cfgio.specialized.typedkeyvalue import TypeAwareKeyValueConfig
import os
from test.keyvalue import TestKeyValueConfig


class TestTypedKVConfig(TestKeyValueConfig):

	def test_parsing(self):
		cfg = TypeAwareKeyValueConfig(os.path.join(os.path.dirname(__file__), 'typedkv.cfg'))

		for key, valuetype in [('astring', str),
								('anint', int),
								('afloat', float),
								('abool', bool),
								('anotherbool', bool),
								('list_of_strings', list)
							]:

			value = cfg.get(key)
			assert value is not None
			assert isinstance(value.value, valuetype)

		l = cfg.get('list_of_strings')
		assert len(l.value) == 3

		for x in l.value:
			assert isinstance(x, str)