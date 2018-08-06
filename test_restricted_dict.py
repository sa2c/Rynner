from restricted_dict import *
import collections
import unittest


class TestRestrictedDictClass(unittest.TestCase):
    def test_can_instantiate(self):
        ro = RestrictedDict()

    def test_disallow_all_by_defauly(self):
        with self.assertRaises(InvalidOptionException):
            ro = RestrictedDict()
            ro['a'] = 5

    def test_can_allow_key(self):
        ro = RestrictedDict(allowed={'a'})
        ro['a'] = 5
        assert ro['a'] == 5

    def test_can_disallow_key(self):
        with self.assertRaises(InvalidOptionException):
            ro = RestrictedDict(allowed={'a'})
            ro['b'] = 5

    def test_can_allow_and_set(self):
        ro = RestrictedDict(options={'a': 'va', 'b': 'vb'}, allowed={'a', 'b'})
        assert ro['b'] == 'vb'
        assert ro['a'] == 'va'

    def test_can_allow_and_reset(self):
        ro = RestrictedDict(options={'a': 'va', 'b': 'vb'}, allowed={'a', 'b'})
        ro['a'] = 'aaa'
        assert ro['a'] == 'aaa'

    def test_first_arg_must_be_iterable(self):
        with self.assertRaises(InvalidDictSpecException):
            RestrictedDict(1)

    def test_allowed_must_be_iterable(self):
        with self.assertRaises(InvalidDictSpecException):
            RestrictedDict(allowed=1)
