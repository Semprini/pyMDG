import unittest

from mdg.uml import UMLAttribute, UMLInstance, UMLPackage
from mdg.render import serialize_instance


class TestJSONOutput(unittest.TestCase):
    def setUp(self):
        self.package = UMLPackage("id", "name")
        self.instance = UMLInstance(self.package, "test1", 1)
        attr = UMLAttribute(self.package, 'testatt', 1)
        attr.value = "testval"
        self.instance.attributes.append(attr)
        self.package.instances.append(self.instance)

    def test_object_serialise(self):
        data = serialize_instance(self.instance)
        self.assertEqual(data['testatt'], 'testval')
