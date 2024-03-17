import unittest

from mdg.tools.case import camelcase, snakecase, pascalcase
from typing import List
from mdg.tools.io import obj_to_dict, dict_to_obj


class TestUMLModel(unittest.TestCase):
    def setUp(self):
        pass

    def test_camel(self):
        self.assertEqual("test", camelcase("test"))
        self.assertEqual("test", camelcase("Test"))
        self.assertEqual("test", camelcase("Test "))
        self.assertEqual("test", camelcase("Test_"))
        self.assertEqual("test", camelcase(" Test_"))
        self.assertEqual("testCase", camelcase("TestCase"))
        self.assertEqual("testCase", camelcase("testCase"))
        self.assertEqual("testCase", camelcase("test case"))
        self.assertEqual("testCase", camelcase("Test Case"))
        self.assertEqual("testCase", camelcase("Test_Case"))


    def test_pascal(self):
        self.assertEqual("Test", pascalcase("test"))
        self.assertEqual("Test", pascalcase("Test"))
        self.assertEqual("TestCase", pascalcase("TestCase"))
        self.assertEqual("TestCase", pascalcase("testCase"))
        self.assertEqual("TestCase", pascalcase("test case"))
        self.assertEqual("TestCase", pascalcase("Test Case"))
        self.assertEqual("TestCase", pascalcase("Test_Case"))


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
    d: dict

    class Meta:
        owned_subobjects = 'my_list'


class TestIO(unittest.TestCase):
    def setUp(self):
        a = foo()
        a.id = 2

        self.b = blort()
        self.b.my_list = [a, ]
        self.b.c = a
        self.b.d = {"e": "f"}

    def test_to_dict(self):
        output = obj_to_dict(self.b)
        self.assertEqual(2, output['my_list'][0]['id'])

    def test_to_obj(self):
        input = {'c': {'id': 1}}
        obj = dict_to_obj(input, blort)
        self.assertEqual(1, obj.c.id)

        input = {'my_list': [{'id': 1}, ], 'c': 1, 'd': {"e": "f"}, 'basic_list': [1, 2, 3]}
        obj = dict_to_obj(input, blort)
        self.assertEqual(1, obj.c.id)
        self.assertEqual('f', obj.d['e'])
        self.assertEqual(2, obj.basic_list[1])
        self.assertEqual(1, obj.my_list[0].id)
