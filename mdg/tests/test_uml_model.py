import unittest

from mdg.uml import UMLClass, UMLPackage, UMLAssociation, Cardinality, UMLAssociationType, UMLAttribute


class TestUMLModel(unittest.TestCase):
    def setUp(self):
        self.root_package = UMLPackage("1", "root")
        child = UMLPackage("2", "child1", self.root_package)
        self.root_package.children.append(child)
        cls = UMLClass(child, "class1", "3")
        child.classes.append(cls)

    def test_find_package(self):
        res = self.root_package.find_by_id("2")
        self.assertEqual(UMLPackage, type(res))
        self.assertEqual("child1", res.name)

    def test_find_class(self):
        res = self.root_package.find_by_id("3")
        self.assertEqual(UMLClass, type(res))
        self.assertEqual("class1", res.name)

    def test_string_to_multiplicity(self):
        assoc = UMLAssociation(self.root_package, self.root_package.children[0].classes[0], self.root_package.children[0].classes[0], 1)
        self.assertEqual(assoc.string_to_multiplicity("0..1"), ("0", "1"))
        self.assertEqual(assoc.string_to_multiplicity("0..*"), ("0", "*"))
        self.assertEqual(assoc.string_to_multiplicity("*..1"), ("*", "1"))

    def test_association_cardinality(self):
        assoc = UMLAssociation(self.root_package, self.root_package.children[0].classes[0], self.root_package.children[0].classes[0], 1)

        assoc.source_multiplicity = ("0", "1")
        assoc.destination_multiplicity = ("0", "*")
        self.assertEqual(assoc.cardinality, Cardinality.ONE_TO_MANY)

        assoc.source_multiplicity = ("0", "1")
        assoc.destination_multiplicity = ("0", "1")
        self.assertEqual(assoc.cardinality, Cardinality.ONE_TO_ONE)

        assoc.source_multiplicity = ("0", "*")
        assoc.destination_multiplicity = ("0", "1")
        self.assertEqual(assoc.cardinality, Cardinality.MANY_TO_ONE)

        assoc.source_multiplicity = ("0", "*")
        assoc.destination_multiplicity = ("0", "*")
        self.assertEqual(assoc.cardinality, Cardinality.MANY_TO_MANY)

    def test_association_type(self):
        assoc = UMLAssociation(self.root_package, self.root_package.children[0].classes[0], self.root_package.children[0].classes[0], 1)
        self.assertEqual(assoc.association_type, UMLAssociationType.ASSOCIATION)
        assoc = UMLAssociation(self.root_package, self.root_package.children[0].classes[0], self.root_package.children[0].classes[0], 1, UMLAssociationType.COMPOSITION)
        self.assertEqual(assoc.association_type, UMLAssociationType.COMPOSITION)

    def test_attribute_type(self):
        attr = UMLAttribute(None, "test", 123)
        attr.set_type('String')
        self.assertEqual(attr.dest_type, 'CharField')
        attr.set_type('String (123)')
        self.assertEqual(attr.dest_type, 'CharField')
        self.assertEqual(attr.length, 123)
        attr.set_type('decimal (12,2)')
        self.assertEqual(attr.dest_type, 'DecimalField')
        self.assertEqual(attr.precision, 12)
        self.assertEqual(attr.scale, 2)

    def test_attribute_get_type(self):
        attr = UMLAttribute(None, "test", 123)
        attr.set_type('String')
        self.assertEqual(attr.get_type('default'), 'string')
