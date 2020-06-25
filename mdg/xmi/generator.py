#!/usr/bin/python
import os
import json

from lxml import etree
from jinja2 import Template, Environment, FileSystemLoader

from mdg.xmi.parse import ns, parse_uml
from mdg.xmi.validator import validate_package
from mdg.config import settings


def output_level_package(env, template_definition, package):
    template = env.get_template(template_definition['source'])
    filename_template = Template(template_definition['dest'])
    filename = os.path.abspath(filename_template.render(package=package))
    dirname = os.path.dirname(filename)

    if not os.path.exists(dirname):
        os.makedirs(dirname)

    # print("Writing: " + filename)
    with open(filename, 'w') as fh:
        fh.write(template.render(package=package))


def output_level_class(env, template_definition, filter_template, package):
    template = env.get_template(template_definition['source'])
    filename_template = Template(template_definition['dest'])
    for cls in package.classes:
        if filter_template is None or filter_template.render(cls=cls) == "True":
            filename = os.path.abspath(filename_template.render(cls=cls))
            dirname = os.path.dirname(filename)
            if not os.path.exists(dirname):
                os.makedirs(dirname)

            # print("Writing: " + filename)
            with open(filename, 'w') as fh:
                fh.write(template.render(cls=cls))


def output_level_enum(env, template_definition, filter_template, package):
    template = env.get_template(template_definition['source'])
    filename_template = Template(template_definition['dest'])

    for enum in package.enumerations:
        if filter_template is None or filter_template.render(enum=enum) == "True":
            filename = os.path.abspath(filename_template.render(enum=enum))
            dirname = os.path.dirname(filename)
            if not os.path.exists(dirname):
                os.makedirs(dirname)

            # print("Writing: " + filename)
            with open(filename, 'w') as fh:
                fh.write(template.render(enum=enum))


def output_level_assoc(env, template_definition, filter_template, package):
    template = env.get_template(template_definition['source'])
    filename_template = Template(template_definition['dest'])

    for assoc in package.associations:
        if filter_template is None or filter_template.render(association=assoc) == "True":
            filename = os.path.abspath(filename_template.render(association=assoc))
            dirname = os.path.dirname(filename)
            if not os.path.exists(dirname):
                os.makedirs(dirname)
            # print("Writing: " + filename)
            with open(filename, 'w') as fh:
                fh.write(template.render(association=assoc))


def output_model(package, recipie_path):
    env = Environment(loader=FileSystemLoader(settings['templates_folder']))
    print("Generating model output")
    for template_definition in settings['templates']:
        filter_template = None
        if 'filter' in template_definition.keys():
            filter_template = Template(template_definition['filter'])

        if template_definition['level'] == 'package':
            if filter_template is None or filter_template.render(package=package) == "True":
                output_level_package(env, template_definition, package)

        elif template_definition['level'] == 'class':
            output_level_class(env, template_definition, filter_template, package)

        elif template_definition['level'] == 'enumeration':
            output_level_enum(env, template_definition, filter_template, package)

        elif template_definition['level'] == 'assocication':
            output_level_assoc(env, template_definition, filter_template, package)

    for child in package.children:
        output_model(child, recipie_path)


def output_test_cases(test_cases):
    print("Generating test case output")
    for case in test_cases:
        serialised = json.dumps(serialize_instance(case), indent=2)

        for template_definition in settings['test_templates']:
            filename_template = Template(template_definition['dest'])
            filename = os.path.abspath(filename_template.render(ins=case))
            dirname = os.path.dirname(filename)
            if not os.path.exists(dirname):
                os.makedirs(dirname)
            # print("Writing: " + filename)
            with open(filename, 'w') as fh:
                fh.write(serialised)


def serialize_instance(instance):
    ret = {}

    for attr in instance.attributes:
        ret[attr.name] = attr.value

    # for assoc in instance.associations_to:
    #    if assoc.source_multiplicity[1] == '*':
    #        if assoc.source.name not in ret.keys():
    #            ret[assoc.source.name] = [serialize_instance(assoc.source),]
    #        else:
    #            ret[assoc.source.name].append(serialize_instance(assoc.source))
    #    else:
    #            ret[assoc.source.name] = serialize_instance(assoc.source)

    for assoc in instance.associations_from:
        if assoc.destination_multiplicity[1] == '*':
            if assoc.destination.name not in ret.keys():
                ret[assoc.destination.name] = [serialize_instance(assoc.destination), ]
            else:
                ret[assoc.destination.name].append(serialize_instance(assoc.destination))
        else:
            ret[assoc.destination.name] = serialize_instance(assoc.destination)

    return ret


def parse(recipie_path):

    # with open(config_filename, 'r') as config_file:
    #    settings = yaml.load(config_file.read(), Loader=yaml.SafeLoader)

    tree = etree.parse(settings['source'])
    model = tree.find('uml:Model', ns)
    root_package = model.xpath("//packagedElement[@name='%s']" % settings['root_package'], namespaces=ns)
    if len(root_package) == 0:
        print("Root packaged element not found. Settings has:{}".format(settings['root_package']))
        return
    root_package = root_package[0]

    model_package, test_cases = parse_uml(root_package, tree)
    print("Base Model Package: " + model_package.name)

    errors = validate_package(model_package)
    if len(errors) > 0:
        print("Validation Errors:")
        for error in errors:
            print("    {}".format(error))

    output_model(model_package, recipie_path)
    output_test_cases(test_cases)
