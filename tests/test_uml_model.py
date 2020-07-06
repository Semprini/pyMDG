import unittest

from mdg.uml import UMLClass, UMLPackage


class TestUMLModel(unittest.TestCase):
    def setUp(self):
        self.root_package = UMLPackage("1", "root")
        child = UMLPackage("2", "child1", self.root_package)
        self.root_package.children.append(child)
        cls = UMLClass(child, "class1", "3")
        child.classes.append(cls)

    def test_find_package(self):
        res = self.root_package.find_by_id("2")
        self.assertEquals(UMLPackage, type(res))
        self.assertEquals("child1", res.name)

    def test_find_class(self):
        res = self.root_package.find_by_id("3")
        self.assertEquals(UMLClass, type(res))
        self.assertEquals("class1", res.name)
