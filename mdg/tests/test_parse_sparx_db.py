import unittest

from lxml import etree

from mdg.parse.sparx_db import attr_parse, class_parse, association_parse
from mdg.uml import UMLClass, UMLPackage, Cardinality, UMLAssociationType

import sqlalchemy
from sqlalchemy.orm import Session

class TestXMIAttributeParse(unittest.TestCase):
    def setUp(self):
        # engine = sqlalchemy.create_engine(f"{settings['source']}", echo=False, future=True)
        # with Session(engine) as session:

        self.package = UMLPackage("id", "name")
        self.parent = UMLClass(self.package, "name", "id")

    def test_sterero_parse(self):
        TXref = "description @STEREO;Name=notifiable;GUID={ADC4E914-13DD-4f1b-A9DB-EDCB89896228};@ENDSTEREO;@STEREO;Name=auditable;GUID={C5DA655B-B862-4a27-96F8-FEB0B2EDD529};@ENDSTEREO;"


class TestXMIClassParse(unittest.TestCase):
    def setUp(self):
        self.package = UMLPackage("id", "name")

    def test_class_parse(self):
        pass

class TestXMIAssociationParse(unittest.TestCase):
    def setUp(self):
        self.package = UMLPackage("id", "name")
        self.source = UMLClass(self.package, "source", "id")
        self.dest = UMLClass(self.package, "dest", "id")

    def test_association_parse(self):
        pass

class TestXMIGeneralizationParse(unittest.TestCase):
    def setUp(self):
        self.package = UMLPackage("id", "name")
        self.generalization = UMLClass(self.package, "source", "12345")

    def test_generalization_parse(self):
        pass
