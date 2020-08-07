Templates
**********

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
for example::

    {% for class in package %}
        {{ class.name }}
    {% endfor %}

With the above hierarchy, the template will be called for 'my model package', 'sub package 1' and 'sub package 2'

Class Mode
----------
In class mode, each class is passed to the template. This is useful when There
is a file output per class - like a POJO file. 

Root Mode
---------
The template will be called once and passed the root package