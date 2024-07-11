import unittest
from typing import List, Optional, cast
from decimal import Decimal

from mdg.tools.case import camelcase, snakecase, pascalcase
from mdg.tools.io import obj_to_dict, dict_to_obj, NestedIOClass


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


class foo(NestedIOClass):
    id: int

    class Meta:
        id_field = 'id'


class blort(NestedIOClass):
    my_list: List[foo]
    basic_list: List[int]
    c: foo
    d: dict
    e: Optional[Decimal]

    class Meta:
        owned_subobjects = List = ['my_list']

    def __init__(self):
        self.e = None

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

    def test_to_obj_simple(self):
        input = {'my_list': [{'id': 1}]}
        obj = dict_to_obj(input, blort)
        self.assertTrue(isinstance(obj,blort))
        obj = cast(blort, obj)
        self.assertEqual(1, obj.my_list[0].id)

    def test_to_obj_full(self):
        input = {'my_list': [{'id': 1}, ], 'c': 1, 'd': {"e": "f"}, 'basic_list': [1, 2, 3],'e': "1.2"}
        obj = dict_to_obj(input, blort)
        self.assertTrue(isinstance(obj,blort))
        obj = cast(blort, obj)
        self.assertTrue(isinstance(obj.my_list[0],foo))
        self.assertTrue(isinstance(obj.d,dict))
        self.assertTrue(isinstance(obj.c,foo))

        self.assertEqual(1, obj.c.id)
        self.assertEqual('f', obj.d['e'])
        self.assertEqual(2, obj.basic_list[1])
        self.assertEqual(1, obj.my_list[0].id)
        self.assertEqual(Decimal("1.2"), obj.e)