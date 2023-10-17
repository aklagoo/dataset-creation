import unittest
from lib.extract import SampleFormatException, extract


class Extract(unittest.TestCase):
    def test_raises_SampleFormatException_on_invalid_error(self):
        self.assertRaises(SampleFormatException, extract, '', '', [{}])
