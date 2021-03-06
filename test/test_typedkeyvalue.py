# -*- coding: utf-8 -*-
import pytest
from cfgio.keyvalue import KeyValueConfigValue
from cfgio.specialized.typedkeyvalue import TypeAwareKeyValueConfig
from test.test_keyvalue import TestKeyValueConfig


class TestTypedKVConfig(TestKeyValueConfig):

	@property
	def default_file(self):
		return 'typedkv.cfg'

	@property
	def cfg_type(self):
		return TypeAwareKeyValueConfig

	@property
	def cfg_value_type(self):
		return KeyValueConfigValue

	@property
	def default_cfg_items(self):
		return [('astring', "This is a string"),
				('anint', 42),
				('afloat', 13.37),
				('abool', True),
				('anotherbool', False),
				('list_of_strings', ["foo", 'bar', "baz"]),
				('another_list', ["foo, bar", 1, 2, 3.4])
				]

	def test_conversion(self):
		cfg = self.cfg_type()

		assert cfg.parse_value('foo', None) is None

		for input, valuetype, expected_value in [
								("This is a string", str, "This is a string"),
								('42', int, 42),
								('13.37', float, 13.37),
								('True', bool, True),
								('on', bool, True),
								('yes', bool, True),
								('false', bool, False),
								('off', bool, False),
								('no', bool, False),
								("""["foo", 'bar', "baz"]""", list, ["foo", 'bar', "baz"]),
								("""["foo, bar", 1, 2, 3.4]""", list, ["foo, bar", 1, 2, 3.4])
							]:

			parsed_value = cfg.parse_value("dummy", input)
			assert parsed_value is not None
			assert isinstance(parsed_value, valuetype)
			assert parsed_value == expected_value

			if isinstance(parsed_value, list):
				assert len(parsed_value) == len(expected_value)
				for i, expected in enumerate(expected_value):
					assert isinstance(parsed_value[i], type(expected))

	def test_format(self):
		cfg = self.cfg_type()

		for raw, expected_s in [
								(42, "42"),
								(13.37, "13.37"),
								(True, "true"),
								(False, "false"),
								(["foo", "bar", "baz"], """[ "foo", "bar", "baz" ]""")
							]:
			assert cfg.format(KeyValueConfigValue('foo', raw)) == "foo=" + expected_s


	def test_write_space_separator(self):
		pass

	def test_read_values_with_space_separator(self):
		pass

	def test_read_quoted_values(self):
		cfg = self.create_config(values_quoted=True)

		x = cfg.get('astring')
		assert x is not None
		assert x.value == "This is a string"