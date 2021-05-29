recipes
=========

The gitgub project has a sample_recipes which has some examples. Each recipe config is in yaml and has the following structure::

    root_package: # <Root package name from modelling tool>
    model_package: # <Model package name within root_package where models are held>
    test_package: # <Test package name within root_package where instances used for test are held>
    source: # <path to exported model - xmi 2.0 or drawio>
    parser: # <either sparx or drawio>
    dest_root: # <base path where to put each generated artifact>
    templates_folder: # <base path where to find custom templates>
    generation_type: # <language to translate attributes into optios are: default, spring data rest, django, marshmallow, sqlalchemy, python, ddl>
    model_templates: # <list of artifacts to generate, see below for details>
    - dest: # <jinja template string which parses to the output file name>
      level: # <package, class, root, copy>
      source: # <path to jinja template file to render>
    test_templates: # <list of test artifacts>

Model Templates Detail
^^^^^^^^^^^^^^^^^^^^^^

In the config yaml for your project there is a list called::
    
    model_templates:

This is a list of files to render based on the parsed classes as discussed in the Metamodel page

Each template item in the list can specify:

- dest: Mandatory. A jinja template string which is passed the package and renders to the output filename
- level: Mandatory. package, class or root - see below for details
- source: Mandatory. Path to the jinja template file
- filter: Optional. A jinja template string which causes the template to be rendered only if the filter renders to "True"

For example here is a django model template entry::

    - dest: "{{package.path}}/models.py"
      level: package
      source: Django/app/models.py.jinja
      filter: "{% if package.classes %}True{% else %}False{% endif %}"

The output file will be based on the package path and the filter will exclude any packages without classes.

Template Levels
^^^^^^^^^^^^^^^

Package Mode
------------
In package mode, each package is passed to the template and the template will 
probably want to iterate over the classes in the package. This is used when 
your output file has multiple data objects defined - like a django models.py

Class Mode
----------
In class mode, each class is passed to the template. This is useful when There
is a file output per class - like a POJO file. 

Root Mode
---------
The template will be called once and passed the root package

Copy Mode
---------
No template will be called, the source file will simply be copied to the destination
