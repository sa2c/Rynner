import unittest
from unittest.mock import patch, MagicMock, call, ANY
from rynner_view import *


class TestRynnerView(unittest.TestCase):
    def setUp(self):
        pass

    def instantiate(self, *args):
        return RynnerView(*args)

    def test_instance(self):
        self.instantiate()

    def test_next(self):
        pass
