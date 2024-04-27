import unittest

from mdg.uml import UMLClass, UMLPackage, UMLAssociation, Cardinality, UMLAssociationType, UMLAttribute, UMLEnumeration, SearchTypes
from mdg.config import defaults


class TestUMLModel(unittest.TestCase):
    def setUp(self):
        self.root_package = UMLPackage("1", "root")
        child = UMLPackage("2", "child1", self.root_package)
        self.root_package.children.append(child)
        self.cls = UMLClass(child, "class1", "3")
        child.classes.append(self.cls)
        cls = UMLClass(child, "class2", "4")
        child.classes.append(cls)
        enum = UMLEnumeration(child, "enum1", "4")
        child.enumerations.append(enum)

    def test_find_package(self):
        res = self.root_package.find_by_id("2")
        assert res is not None
        self.assertEqual(UMLPackage, type(res))
        self.assertEqual("child1", res.name)

    def test_find_enumeration(self):
        # Check that we don't find the wrong thing
        res = self.root_package.find_by_id("3", SearchTypes.ENUM)
        self.assertEqual(None, res)
        # Check that we find the enum with the id=4, not the class with id=4
        res = self.root_package.find_by_id("4", SearchTypes.ENUM)
        assert res is not None
        self.assertEqual(UMLEnumeration, type(res))
        self.assertEqual("enum1", res.name)

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
        attr = UMLAttribute(self.cls, "test", 123)
        attr.set_type('String')
        self.assertEqual(attr.dest_type, 'CharField')
        self.assertEqual(attr.length, defaults[ "default_string_length"])
        attr.set_type('String (123)')
        self.assertEqual(attr.dest_type, 'CharField')
        self.assertEqual(attr.length, 123)
        attr.set_type('decimal (12,2)')
        self.assertEqual(attr.dest_type, 'DecimalField')
        self.assertEqual(attr.precision, 12)
        self.assertEqual(attr.scale, 2)

    def test_attribute_get_type(self):
        attr = UMLAttribute(self.cls, "test", 123)
        attr.set_type('String')
        self.assertEqual(attr.get_type('default'), 'string')

    def test_get_all_(self):
        self.assertEqual(len(self.root_package.get_all_classes()), 2)
        self.assertEqual(len(self.root_package.get_all_enums()), 1)


class TestUMLClassFunctions(unittest.TestCase):
    def setUp(self):
        self.root_package = UMLPackage("1", "root")
        child = UMLPackage("2", "child1", self.root_package)
        self.root_package.children.append(child)

        # Ceate class to be specialized by with an attribute
        cls = UMLClass(child, "class1", "3")
        child.classes.append(cls)
        att = UMLAttribute(cls, "foo", 4)
        cls.attributes.append(att)

        # Create simple class with no attributes
        cls = UMLClass(child, "class2", "4")
        child.classes.append(cls)

        # Create inheitance
        child.classes[1].generalization = child.classes[0]
        child.classes[0].specialized_by.append(child.classes[1])       # TODO: Setter function which does this linking

    def test_find_class(self):
        res = self.root_package.find_by_id("3", SearchTypes.CLASS)
        assert res is not None
        self.assertEqual(UMLClass, type(res))
        self.assertEqual("class1", res.name)

    def test_get_all_attributes(self):
        # Grab class which inheits fom a class
        cls = self.root_package.children[0].classes[1]
        self.assertEqual("class2", cls.name)

        # Inherited class is not abstact so expect an empty result set
        res = cls.get_all_attributes(abstract_only=True)
        self.assertEqual([], res)

        # Include attributes of non abstract class so expect an attribute
        res = cls.get_all_attributes(abstract_only=False)
        self.assertEqual(1, len(res))
