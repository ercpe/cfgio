# -*- coding: utf-8 -*-
from ..keyvalue import KeyValueConfig


class TypeAwareKeyValueConfig(KeyValueConfig):

	def __init__(self, filename, comment_chars=['#', ';']):
		super(TypeAwareKeyValueConfig, self).__init__(filename, comment_chars=comment_chars, values_quoted=False)

	def parse(self, line):
		kvcv = super(TypeAwareKeyValueConfig, self).parse(line)

		if not kvcv:
			return None

		kvcv.value = self.parse_value(kvcv.value)

		return kvcv

	def parse_value(self, s):
		if s is None:
			return None

		if self.is_quoted(s):
			return str(s[1:-1])
		else:
			if s.startswith("[") and s.endswith("]"):
				l = []

				value_string = s.strip().lstrip("[").rstrip("]")

				# FIXME: this breaks easily
				for item in [x.strip() for x in value_string.split(",")]:
					l.append(self.parse_value(item))

				return l
			else:
				for f in [int, float, complex, bool]:
					try:
						return f(s)
					except ValueError:
						pass