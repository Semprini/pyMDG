import os
import json
import re
import yaml

from mdg.uml import UMLPackage, UMLClass, UMLEnumeration, UMLInstance, UMLAssociation, UMLAttribute

ns={
	'uml':'http://schema.omg.org/spec/UML/2.1',
	'xmi':'http://schema.omg.org/spec/XMI/2.1',
    'thecustomprofile':'http://www.sparxsystems.com/profiles/thecustomprofile/1.0',
    'NIEM_PSM_profile':'http://www.omg.org/spec/NIEM-UML/20130801/NIEM_PSM_Profile',
}

settings = None

def parse_uml(element, root):
    """ Root package parser entrypoint.
    """
    global settings
    model_package = None
    test_package = None
    
    with open(os.environ.get('PYXMI_SETTINGS_MODULE'), 'r') as config_file:
        settings=yaml.load(config_file.read(), Loader=yaml.SafeLoader)


    # Find the element that is the root for models
    print( "Parsing models" )
    model_element=element.xpath("//packagedElement[@name='%s']"%settings['model_package'], namespaces=ns)
    if len(model_element) == 0:
        raise ValueError("Model packaged element not found. Settings has:{}".format(settings['model_package']))
    model_element=model_element[0]

    # Create our root model UMLPackage and parse in 3 passes
    e_type = model_element.get('{%s}type'%ns['xmi'])
    if e_type == 'uml:Package':
        model_package = UMLPackage()
        UMLPackage_parse(model_package, model_element, root)
        UMLPackage_parse_inheritance(model_package)
        UMLPackage_parse_associations(model_package)
    else:
        raise ValueError('Error - Non uml:Package element provided to packagedElement parser')

    # Find the element that is the root for test data
    print( "Parsing test cases" )
    test_element=element.xpath("//packagedElement[@name='%s']"%settings['test_package'], namespaces=ns)
    if len(test_element) == 0:
        raise ValueError("Test packaged element not found. Settings has:{}".format(settings['test_package']))
    test_element=test_element[0]

    # Create our root test data UMLPackage and parse in 2 passes. Does not support inheritance
    e_type = test_element.get('{%s}type'%ns['xmi'])
    if e_type == 'uml:Package':
        test_package = UMLPackage()
        UMLPackage_parse(test_package, test_element, root)
        UMLPackage_parse_associations(test_package)

    # With our test package parsed, we must return a list of instances instead of hierarchy of packages
    test_cases = parse_test_cases(test_package)
    return model_package, test_cases


def parse_test_cases(package):
    """ Looks through package hierarchy for instances with request or response stereotype
    and returns list of instances.
    """
    test_cases = []
    
    for instance in package.instances:
        if instance.stereotype in ['request','response']:
            test_cases.append(instance)
    
    for child in package.children:
        res = parse_test_cases(child)
        if res != []:
            test_cases += res
    
    return test_cases


def UMLPackage_parse(package, element, root):
        """ Extract package details, call class parser for classes and self parser for sub-packages.
        Associations are not done here, but in a 2nd pass using the parse_associations function.
        """
        package.name = element.get('name')
        package.id = element.get('{%s}id'%ns['xmi'])
        package.element = element
        package.root_element = root

        # Package path is hierarchical. Add the current path onto it's parent
        if package.parent is None:
            package.path = '/'
        else:
            package.path = package.parent.path + package.name + '/'

        #Detail is sparx sprecific
        #TODO: Put modelling tool in settings and use tool specific parser here
        detail = root.xpath("//element[@xmi:idref='%s']"%package.id, namespaces=ns)[0]
        properties = detail.find('properties')
        package.stereotype = properties.get('stereotype')
        if package.stereotype is not None:
            package.inherited_stereotypes.append([package.stereotype,package])

        # Loop through all child elements and get classes and sub packages
        for child in element:
            e_type = child.get('{%s}type'%ns['xmi'])
            
            if e_type == 'uml:Package':
                pkg = UMLPackage(package)
                UMLPackage_parse(pkg, child, root)
                package.children.append( pkg )

            elif e_type == 'uml:Class':
                cls = UMLClass(package)
                UMLClass_parse(cls, child, root)
                if cls.name is not None:
                    package.classes.append( cls )

            elif e_type == 'uml:InstanceSpecification':
                ins = UMLInstance(package)
                UMLInstance_parse(ins, child, root)
                if ins.name is not None:
                    package.instances.append( ins )
 
            elif e_type == 'uml:Enumeration':
                enum = UMLEnumeration(package)
                UMLEnumeration_parse(enum, child, root)
                if enum.name is not None:
                    package.enumerations.append( enum )
  
        #print("Parsed package with {} classes & {} instances: {}{}".format( len(package.classes), len(package.instances), package.path, package.name ) )
        

    def parse_associations(self):
        """ Packages and classes should already have been parsed so now we link classes for each association.
        This gets messy as XMI output varies based on association type. 
        This supports both un-specified and source to destination directional associations
        """
        for child in self.element:
            e_type = child.get('{%s}type'%ns['xmi'])
            e_id = child.get('{%s}id'%ns['xmi'])
            
            if e_type == 'uml:Association':
                assoc_source_id = None
                assoc_dest_id = None
                for assoc in child:
                    # If unspecified direction then both source and destination info are child elements within the association
                    assoc_type = assoc.get('{%s}type'%ns['xmi'])
                    assoc_id = assoc.get('{%s}id'%ns['xmi'])
                    if assoc_id is not None and assoc_type == 'uml:Property' and assoc_id[:8] == 'EAID_src':
                        assoc_source_elem = assoc
                        assoc_source_type_elem = assoc.find('type')
                        assoc_source_id = assoc_source_type_elem.get('{%s}idref'%ns['xmi'])
                    if assoc_id is not None and assoc_type == 'uml:Property' and assoc_id[:8] == 'EAID_dst':
                        assoc_dest_elem = assoc
                        assoc_dest_type_elem = assoc.find('type')
                        assoc_dest_id = assoc_dest_type_elem.get('{%s}idref'%ns['xmi'])
                
                # If association direction is source to destination then 
                # destination class info is found as an ownedAttribute in the source element
                if assoc_dest_id is None:
                    for assoc in child:
                        if assoc.tag == 'memberEnd':
                            assoc_idref = assoc.get('{%s}idref'%ns['xmi'])
                            if assoc_idref[:8] == 'EAID_dst':
                                try:
                                    assoc_dest_elem = self.root_element.xpath("//ownedAttribute[@xmi:id='%s']"%assoc_idref, namespaces=ns)[0]
                                except IndexError as e:
                                    print("Failed to find member end association destination. Id: {}".format(assoc_idref))
                                    raise
                                assoc_dest_type_elem = assoc_dest_elem.find('type')
                                assoc_dest_id = assoc_dest_type_elem.get('{%s}idref'%ns['xmi'])
                
                #print("association: src id={} dest id={}".format(assoc_source_id,assoc_dest_id))
                # TODO: Raise error if we don't have a source and dest
                source = self.root_package.find_by_id(assoc_source_id)
                dest = self.root_package.find_by_id(assoc_dest_id)
                if source is not None and dest is not None:
                    association = UMLAssociation(self, source, dest)
                    association.parse(child, assoc_source_elem, assoc_dest_elem)
                    self.associations.append(association)
                else:
                    print("Unable to create association id={}".format(e_id))

        for child in self.children:
            child.parse_associations()


    def parse_inheritance(self):
        """ Looks for classes with a supertype and finds the correct object """
        for cls in self.classes:
            if cls.supertype_id is not None:
                cls.supertype = self.root_package.find_by_id(cls.supertype_id)
                cls.supertype.is_supertype = True
                if cls.id_attribute is None:
                    cls.id_attribute = cls.supertype.id_attribute
        
            for attr in cls.attributes:
                if attr.classification_id is not None:
                    attr.classification = self.root_package.find_by_id(attr.classification_id)
        
        for child in self.children:
            child.parse_inheritance()


class UMLInstance(object):
    def __init__(self, package):
        self.attributes = []
        self.associations_from = []
        self.associations_to = []
        self.package = package
        self.stereotype = None

    def parse(self, element, root):
        self.name = element.get('name')
        self.id = element.get('{%s}id'%ns['xmi'])

        #Detail is sparx sprecific
        #TODO: Put modelling tool in settings and use tool specific parser here
        detail = root.xpath("//element[@xmi:idref='%s']"%self.id, namespaces=ns)[0]
        properties = detail.find('properties')
        self.stereotype = properties.get('stereotype')
        
        # Create attributes for each item found in the runstate
        # TODO: Change this to using an re
        extendedProperties = detail.find('extendedProperties')
        if extendedProperties.get('runstate') is not None:
            runstate = extendedProperties.get('runstate')
            vars = runstate.split('@ENDVAR;')
            for var in vars:
                if var != '':
                    variable,value=(var.split(';')[1:3])
                    attr = UMLAttribute(self)
                    attr.name = variable.split('=')[1]
                    attr.value = value.split('=')[1]
                    self.attributes.append( attr )
                    

class UMLAssociation(object):
    def __init__(self, package, source, dest):
        self.package = package
        self.source = source
        self.dest = dest
        source.associations_from.append(self)
        dest.associations_to.append(self)
        self.source_multiplicity = ['0','0']
        self.dest_multiplicity = ['0','0']
        self.association_type = None
        
    def source_nameCamel(self):
        return re.sub(r'_([a-z])', lambda x: x.group(1).upper(), self.source_name)

    def dest_nameCamel(self):
        return re.sub(r'_([a-z])', lambda x: x.group(1).upper(), self.dest_name)
        
    def parse(self, element, source_element, dest_element):
        
        # Extract multiplicity for source
        source_lower = source_element.find('lowerValue')
        if source_lower is not None:
            source_lower = source_lower.get('value')
            if source_lower == '-1':
                source_lower = '*'
            source_upper = source_element.find('upperValue').get('value')
            if source_upper == '-1':
                source_upper = '*'
            self.source_multiplicity = (source_lower, source_upper)

        # Extract multiplicity for dest
        dest_lower = dest_element.find('lowerValue')
        if dest_lower is not None:
            dest_lower = dest_lower.get('value')
            if dest_lower == '-1':
                dest_lower = '*'
            dest_upper = dest_element.find('upperValue').get('value')
            if dest_upper == '-1':
                dest_upper = '*'
            self.dest_multiplicity = (dest_lower, dest_upper)
        
        #print( '{}:{} to {}:{}'.format(self.source.name, self.source_multiplicity, self.dest.name, self.dest_multiplicity))
        
        # Use multiplicities to calculate the type of association
        if self.source_multiplicity[1] == '*' and self.dest_multiplicity[1] in ('0','1'):
            self.association_type = 'ManyToOne'
        elif self.dest_multiplicity[1] == '*' and self.source_multiplicity[1] in ('0','1'):
            self.association_type = 'OneToMany'
        elif self.dest_multiplicity[1] == '*' and self.source_multiplicity[1] == '*':
            self.association_type = 'ManyToMany'
        elif self.dest_multiplicity[1] in ('0','1') and self.source_multiplicity[1] in ('0','1'):
            self.association_type = 'OneToOne'

        # If it's an association to or from a multiple then pluralize the name
        # TODO: Allow pluralized name to be specified in UML
        if dest_element.get('name') is not None:
            self.dest_name = dest_element.get('name')
        else:
            # Use opposing ends class name as attribute name for association
            self.dest_name = self.source.name.lower()
            if self.source_multiplicity[1] == '*':
                self.dest_name += 's'
            
        if source_element.get('name') is not None:
            self.source_name = source_element.get('name')
        else:
            # Use opposing ends class name as attribute name for association
            self.source_name = self.dest.name.lower()
            if self.dest_multiplicity[1] == '*':
                self.source_name += 's'
                
        #print('Assoc in {}: {} to {}: type = {}'.format(self.source.name, self.source_name, self.dest_name, self.association_type) )

class UMLEnumeration(object):
    def __init__(self, package):
        self.values = []
        self.package = package
        
    def parse(self, element, root):
        self.name = element.get('name')
        self.id = element.get('{%s}id'%ns['xmi'])

        # Loop through class elements children for values.
        for child in element:    
            e_type = child.get('{%s}type'%ns['xmi'])
            if e_type == 'uml:EnumerationLiteral':
                self.values.append(child.get('name'))


class UMLClass(object):
    def __init__(self, package):
        self.attributes = []
        self.associations_from = []
        self.associations_to = []
        self.package = package
        self.supertype = None
        self.supertype_id = None
        self.is_supertype = False
        self.stereotypes = []
        self.id_attribute = None
        
        for inherited_stereotype, inherited_package in package.inherited_stereotypes:
            if not hasattr(self,inherited_stereotype):
                setattr(self, inherited_stereotype, inherited_package )


    def parse(self, element, root):
        self.name = element.get('name')
        self.id = element.get('{%s}id'%ns['xmi'])
        if element.get('isAbstract') == 'true':
            self.is_abstract = True
        else:
            self.is_abstract = False

        # If the class is inherited from a superclass then get the ID. The actual object will be found in a separate pass as it may not have been parsed yet
        supertype_element = element.find('generalization')
        if supertype_element is not None:
            self.supertype_id = supertype_element.get('general')

        # Loop through class elements children for attributes.
        for child in element:    
            e_type = child.get('{%s}type'%ns['xmi'])

            if e_type == 'uml:Property':
                # Associations will be done in a separate pass
                if child.get('association') is None and child.get('name') is not None:
                    cls = UMLAttribute(self)
                    cls.parse(child, root)
                    self.attributes.append( cls )

        # Detail is sparx sprecific
        #TODO: Put modelling tool in settings and use tool specific parser here
        detail = root.xpath("//element[@xmi:idref='%s']"%self.id, namespaces=ns)[0]

        # Get stereotypes, when multiple are provided only the first is found in the stereotype tag but all are found in xrefs
        xrefs = detail.find('xrefs')
        value = xrefs.get('value')
        if value is not None:
            self.stereotypes = re.findall('@STEREO;Name=(.*?);', value)


class UMLAttribute(object):
    def __init__(self, parent=None):
        self.parent = parent
        self.is_unique = False
        self.stereotype = None
        self.classification = None
        self.classification_id = None


    def nameCamel(self):
        return re.sub(r'_([a-z])', lambda x: x.group(1).upper(), self.name)


    def parse(self, element, root):
        global settings
        
        self.name = element.get('name')
        self.id = element.get('{%s}id'%ns['xmi'])
        self.visibility = element.get('visibility')
        type_elem = element.find('type')
        type_id = type_elem.get('{%s}idref'%ns['xmi'])
        if type_id[:4]=='EAID':
            self.classification_id = type_id
        
        #Detail is sparx sprecific
        #TODO: Put modelling tool in settings and use tool specific parser here
        detail = root.xpath("//attribute[@xmi:idref='%s']"%self.id, namespaces=ns)[0]
        properties = detail.find('properties')
        self.type = properties.get('type')
        
        
        if properties.get('type') in settings['types'].keys():
            self.dest_type = settings['types'][properties.get('type')]
        else:
            self.dest_type = properties.get('type')
            
        xrefs = detail.find('xrefs')
        if xrefs.get('value') is not None and 'NAME=isID' in xrefs.get('value'):
            self.is_id = True
            self.parent.id_attribute = self
        else:
            self.is_id = False
            
        #Todo: decide how to include string lengths in UML
        if self.type == 'string':
            self.length = 100

        stereotype = detail.find('stereotype')
        if stereotype is not None:
            self.stereotype = stereotype.get('stereotype')
        
        constraints = detail.find('Constraints')
        if constraints is not None:
            for constraint in constraints:
                name=constraint.get('name')
                if name == 'unique':
                    self.is_unique = True
                elif name.startswith('length'):
                    self.length=int(name.split("=")[1])
        