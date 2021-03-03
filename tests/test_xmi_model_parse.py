import unittest

from lxml import etree

from mdg.sparx_xmi.parse import attr_parse, class_parse
from mdg.uml import UMLClass, UMLPackage


class TestXMIAttributeParse(unittest.TestCase):
    def setUp(self):
        self.tree = etree.fromstring("""
                    <xmi:XMI xmi:version="2.1" xmlns:uml="http://schema.omg.org/spec/UML/2.1" xmlns:xmi="http://schema.omg.org/spec/XMI/2.1" xmlns:thecustomprofile="http://www.sparxsystems.com/profiles/thecustomprofile/1.0">
                        <ownedAttribute xmi:type="uml:Property" xmi:id="EAID_7EBDF95C_3A97_4163_A683_3ACC3CF507E4" name="system" visibility="private" isStatic="false" isReadOnly="false" isDerived="false" isOrdered="false" isUnique="true" isDerivedUnion="false">
                            <type xmi:idref="EAJava_int"/>
                        </ownedAttribute>
                        <attribute xmi:idref="EAID_7EBDF95C_3A97_4163_A683_3ACC3CF507E4" name="id" scope="Private">
                            <initial/>
                            <documentation/>
                            <model ea_localid="1213" ea_guid="{47318F66-BBA6-4e9f-9045-83B2E12E25C8}"/>
                            <properties type="int" precision="0" collection="false" length="0" static="0" duplicates="0" changeability="changeable"/>
                            <coords ordered="0" scale="0"/>
                            <containment containment="Not Specified" position="0"/>
                            <stereotype/>
                            <bounds lower="1" upper="1"/>
                            <options/>
                            <style/>
                            <styleex value="volatile=0;"/>
                            <tags/>
                            <xrefs value="$XREFPROP=$XID={EA9F1375-D590-4c2b-8721-DC0B55BFE4A9}$XID;$NAM=CustomProperties$NAM;$TYP=attribute property$TYP;$VIS=Public$VIS;$PAR=0$PAR;$DES=@PROP=@NAME=isID@ENDNAME;@TYPE=Boolean@ENDTYPE;@VALU=1@ENDVALU;@PRMT=@ENDPRMT;@ENDPROP;$DES;$CLT={47318F66-BBA6-4e9f-9045-83B2E12E25C8}$CLT;$SUP=&lt;none&gt;$SUP;$ENDXREF;"/>
                        </attribute>
                    </xmi:XMI>""")
        self.package = UMLPackage("id", "name")
        self.parent = UMLClass(self.package, "name", "id")

    def test_attr_parse(self):
        element = self.tree.find("ownedAttribute")
        self.assertIsNotNone(element)

        attr = attr_parse(self.parent, element, self.tree)
        self.assertIsNotNone(attr)
        self.assertEqual(attr.classification_id, None)


class TestXMIClassParse(unittest.TestCase):
    def setUp(self):
        self.tree = etree.fromstring("""
                    <xmi:XMI xmi:version="2.1" xmlns:uml="http://schema.omg.org/spec/UML/2.1" xmlns:xmi="http://schema.omg.org/spec/XMI/2.1" xmlns:thecustomprofile="http://www.sparxsystems.com/profiles/thecustomprofile/1.0">
                        <packagedElement xmi:type="uml:Class" xmi:id="EAID_5A9CB912_F283_41ae_9E4D_D73598C576AE" name="ExternalReference" visibility="public" isAbstract="true">
                        </packagedElement>
                        <element xmi:idref="EAID_5A9CB912_F283_41ae_9E4D_D73598C576AE" xmi:type="uml:Class" name="ExternalReference" scope="public">
                            <model package="EAPK_EA154075_33FD_455d_B07A_FCBD08A7882D" tpos="0" ea_localid="664" ea_eleType="element"/>
                            <properties isSpecification="false" sType="Class" nType="0" scope="public" isRoot="false" isLeaf="false" isAbstract="true" isActive="false"/>
                            <project author="atkinp" version="1.0" phase="1.0" created="2019-07-24 08:42:52" modified="2020-06-23 19:23:20" complexity="1" status="Proposed"/>
                            <code gentype="Java"/>
                            <style appearance="BackColor=-1;BorderColor=-1;BorderWidth=-1;FontColor=-1;VSwimLanes=1;HSwimLanes=1;BorderStyle=0;"/>
                            <tags/>
                            <xrefs/>
                            <extendedProperties tagged="0" package_name="Common"/>
                        </element>
                    </xmi:XMI>""")
        self.package = UMLPackage("id", "name")

    def test_class_parse(self):
        element = self.tree.find("packagedElement")
        self.assertIsNotNone(element)

        clazz = class_parse(self.package, element, self.tree)
        self.assertIsNotNone(clazz)
        self.assertEqual(clazz.is_abstract, True)
        self.assertEqual(clazz.status, "Proposed")