import unittest

from mdg.uml import UMLAttribute, UMLClass, UMLPackage, UMLAssociation
from mdg.uml import dumps as uml_dumps


class TestDumps(unittest.TestCase):
    def setUp(self):
        self.package = UMLPackage("id", "name")

        cls1 = UMLClass(self.package, "test1", 1)
        attr = UMLAttribute(cls1, 'Test Att', 2)
        cls1.attributes.append(attr)
        attr = UMLAttribute(cls1, 'Test Att 2', 3)
        cls1.attributes.append(attr)

        cls2 = UMLClass(self.package, "test2", 4)
        attr = UMLAttribute(cls2, 'Test Att 3', 5)
        cls2.attributes.append(attr)
        attr = UMLAttribute(cls2, 'Test Att 4', 6)
        cls2.attributes.append(attr)

        self.package.classes.append(cls1)
        self.package.classes.append(cls2)

        assoc = UMLAssociation(self.package, cls1, cls2, 7)
        self.package.associations.append(assoc)

    def test_object_serialise(self):
        data: str = uml_dumps(self.package)
        self.assertGreater(data.find('"associations": [{'), -1)
