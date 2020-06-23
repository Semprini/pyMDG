import unittest

from lxml import etree

from mdg.xmi.parse import attr_parse
from mdg.uml import UMLClass, UMLPackage

class TestXMIParse(unittest.TestCase):
    def setUp(self):
        self.tree = etree.fromstring("""
                    <xmi:XMI xmi:version="2.1" xmlns:uml="http://schema.omg.org/spec/UML/2.1" xmlns:xmi="http://schema.omg.org/spec/XMI/2.1" xmlns:thecustomprofile="http://www.sparxsystems.com/profiles/thecustomprofile/1.0">
                        <ownedAttribute xmi:type="uml:Property" xmi:id="EAID_7EBDF95C_3A97_4163_A683_3ACC3CF507E4" name="system" visibility="private" isStatic="false" isReadOnly="false" isDerived="false" isOrdered="false" isUnique="true" isDerivedUnion="false">
							<lowerValue xmi:type="uml:LiteralInteger" xmi:id="EAID_LI000003_3A97_4163_A683_3ACC3CF507E4" value="1"/>
							<upperValue xmi:type="uml:LiteralInteger" xmi:id="EAID_LI000004_3A97_4163_A683_3ACC3CF507E4" value="1"/>
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
        self.root = self.tree
        self.package = UMLPackage("id","name")
        self.parent = UMLClass(self.package, "name", "id")


    def test_attr_parse(self):
        element = self.tree.find("ownedAttribute")

        attr = attr_parse(self.parent, element, self.root)
        self.assertNotEqual(attr, None)



