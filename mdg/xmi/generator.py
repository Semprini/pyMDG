#!/usr/bin/python
import json
import os

from jinja2 import Environment, FileSystemLoader, Template
from lxml import etree

from mdg.config import settings
from mdg.util import camelcase, snakecase, titlecase, sentencecase
from mdg.xmi.parse import ns, parse_uml
from mdg.xmi.validator import validate_package


def output_level_package(env, source_template, dest_file_template, package) -> None:
    dest_filename = os.path.abspath(dest_file_template.render(package=package))
    dirname = os.path.dirname(dest_filename)

    if not os.path.exists(dirname):
        os.makedirs(dirname)

    with open(dest_filename, 'w') as fh:
        fh.write(source_template.render(package=package))


def output_level_class(env, source_template, dest_file_template, filter_template, package):

    for cls in package.classes:
        if filter_template is None or filter_template.render(cls=cls) == "True":
            filename = os.path.abspath(dest_file_template.render(cls=cls))
            dirname = os.path.dirname(filename)
            if not os.path.exists(dirname):
                os.makedirs(dirname)

            with open(filename, 'w') as fh:
                fh.write(source_template.render(cls=cls))


def output_level_enum(env, source_template, dest_file_template, filter_template, package):

    for enum in package.enumerations:
        if filter_template is None or filter_template.render(enum=enum) == "True":
            filename = os.path.abspath(dest_file_template.render(enum=enum))
            dirname = os.path.dirname(filename)
            if not os.path.exists(dirname):
                os.makedirs(dirname)

            with open(filename, 'w') as fh:
                fh.write(source_template.render(enum=enum))


def output_level_root(env, source_template, dest_file_template, package):
    dest_filename = os.path.abspath(dest_file_template.render(package=package))
    dirname = os.path.dirname(dest_filename)

    if not os.path.exists(dirname):
        os.makedirs(dirname)

    with open(dest_filename, 'w') as fh:
        fh.write(source_template.render(package=package))


def output_level_assoc(env, source_template, dest_file_template, filter_template, package):

    for assoc in package.associations:
        if filter_template is None or filter_template.render(association=assoc) == "True":
            filename = os.path.abspath(dest_file_template.render(association=assoc))
            dirname = os.path.dirname(filename)
            if not os.path.exists(dirname):
                os.makedirs(dirname)

            with open(filename, 'w') as fh:
                fh.write(source_template.render(association=assoc))


def output_model(package):
    env = Environment(loader=FileSystemLoader(settings['templates_folder']))
    env.filters['camelcase'] = camelcase
    env.filters['snakecase'] = snakecase
    env.filters['titlecase'] = titlecase
    env.filters['sentencecase'] = sentencecase

    print("Generating model output for package {}".format(package.path))
    for template_definition in settings['model_templates']:
        source_template = env.get_template(template_definition['source'])
        dest_file_template = Template(os.path.join(settings['dest_root'], template_definition['dest']))
        filter_template = None
        if 'filter' in template_definition.keys():
            filter_template = Template(template_definition['filter'])

        if template_definition['level'] == 'package':
            if filter_template is None or filter_template.render(package=package) == "True":
                output_level_package(env, source_template, dest_file_template, package)

        elif template_definition['level'] == 'class':
            output_level_class(env, source_template, dest_file_template, filter_template, package)

        elif template_definition['level'] == 'enumeration':
            output_level_enum(env, source_template, dest_file_template, filter_template, package)

        elif template_definition['level'] == 'assocication':
            output_level_assoc(env, source_template, dest_file_template, filter_template, package)

        elif template_definition['level'] == 'root' and package.parent is None:
            output_level_root(env, source_template, dest_file_template, package)

    for child in package.children:
        output_model(child)


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


def parse():
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

    output_model(model_package)
    output_test_cases(test_cases)
