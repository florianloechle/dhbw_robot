import unittest
import shared.utils as utils

testBreakPoints = {
    "1": 4.5,
    "2": 29,
    "3": 51,
    "4": 76
}


class TestUtilsMethods(unittest.TestCase):

    def test_returns_next_breakpoint(self):
        self.assertEqual(utils.get_next_breakpoint(
            6.3434, testBreakPoints), 29)
        self.assertEqual(utils.get_next_breakpoint(43.34, testBreakPoints), 51)
        self.assertEqual(utils.get_next_breakpoint(
            51.4542, testBreakPoints), 76)

    def test_omit_range(self):
        print(utils.omit_range(38,32,4))
        self.assertEqual(utils.omit_range(38, 32, 4), 32)
        self.assertEqual(utils.omit_range(32, 38, 4), 38)
        self.assertEqual(utils.omit_range(34, 32, 4), 34)
