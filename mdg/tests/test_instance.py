import unittest

from mdg.uml import UMLAttribute, UMLInstance, UMLPackage
from mdg.generate.render import serialize_instance


class TestInstanceOutput(unittest.TestCase):
    def setUp(self):
        self.package = UMLPackage("id", "name")
        self.instance = UMLInstance(self.package, "test1", 1)

        attr = UMLAttribute(self.package, 'Test Att', 1)
        attr.value = 'testval'
        self.instance.attributes.append(attr)

        attr = UMLAttribute(self.package, 'Test Att 2', 2)
        attr.value = 10
        self.instance.attributes.append(attr)

        self.package.instances.append(self.instance)

    def test_object_serialise(self):
        data = serialize_instance(self.instance)
        self.assertEqual(data['test_att'], 'testval')

        self.assertEqual(data['test_att_2'], 10)
