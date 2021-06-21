import unittest

from mdg.tools.case import camelcase, snakecase
from typing import List
from mdg.tools.io import obj_to_dict, dict_to_obj


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


class foo:
    id: int

    class Meta:
        id_field = 'id'


class blort:
    my_list: List[foo]
    basic_list: List[int]
    c: foo

    class Meta:
        owned_subobjects = 'my_list'


class TestIO(unittest.TestCase):
    def setUp(self):
        a = foo()
        a.id = 2

        self.b = blort()
        self.b.my_list = [a, ]
        self.b.c = a

    def test_to_dict(self):
        output = obj_to_dict(self.b)
        self.assertEqual(2, output['my_list'][0]['id'])

    def test_to_obj(self):
        input = {'my_list': [{'id': 2}], 'basic_list': [1, 2, 3]}
        obj = dict_to_obj(input, blort)
        self.assertEqual(2, obj.my_list[0].id)
