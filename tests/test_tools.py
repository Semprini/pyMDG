import unittest

from mdg.tools.case import camelcase, snakecase


class TestUMLModel(unittest.TestCase):
    def setUp(self):
        pass

    def test_camel(self):
        self.assertEqual("TestCase", camelcase("TestCase"))
        self.assertEqual("TestCase", camelcase("testCase"))
        self.assertEqual("TestCase", camelcase("test case"))
        self.assertEqual("TestCase", camelcase("Test Case"))
        self.assertEqual("TestCase", camelcase("Test_Case"))

    def test_snake(self):
        self.assertEqual("test_case", snakecase("testCase"))
        self.assertEqual("test_case", snakecase("test_case"))
        self.assertEqual("test_case", snakecase("TestCase"))
        self.assertEqual("test_case", snakecase("test case"))
        self.assertEqual("test_case", snakecase("Test Case"))
        self.assertEqual(None, snakecase(None))
        self.assertEqual("eftpos", snakecase("EFTPOS"))
