Output Templates
================

pyMDG's purpose is to allow a set of business rules to be used to generate physical attributes from logical models. The business rules are codified into the Jinja2 templates. 

The project has a set of templates provided in the mdg/templates folders. These should be seen as a starting point, as your set of business rules will probably be specific to your business. pyMDG will use these templates if a template is not found in the path from 'templates_folder' in your settings file.

A template is rendered by specifying it in a recipe and calling mdg-tool generate <settings file name>. Easiest way to start with your template is to grab one of the samples and drag it into your projects templates_folder, you can then start adding your specifics.

Each settings file has a list of generation_artifacts. Each element in this list will use a specific template to render one or more artifacts based on the specified 'level' - see the Model Template Levels section in the recipies doc page. 

Passed into the template will be either a "package" or a "cls" argument. The provided argument will conform to the Metamodel. Check the metatmodel page in the docs for more info on the fields and functions available.

Here's an example of generating a list of classes in a package::

    {% for cls in package.classes %}
        {{ cls.name }}
    {% endfor %}

With the recipe specifying the above template at package level, we would get a file generated for each UML package containing just the names of the classes in the package.

Sample Templates
^^^^^^^^^^^^^^^^

Hasura
------

    path: mdg/templates/hasura.json.jinja

This template is designed to be called once. The typical use will be to configure the generation artifact at "root" level - as seen the in the sample in "sample_receipes/sparxdb/config-sparxdb-graphql.yaml"

The template expects a DB table per object found in each packagge in the form of: {{ cls.package.name }}_{{ cls.name }}

The template supports many to one, one to many, one to one and many to many relationships. In the case of many to many, the template expects an intermediary table named based on the source object and destination object and the names of their packages. A key part of the modelling nomenclature is that direction of a relationship is important and specifies ownership/dependency.

Each object must have a id field modelled which is translated into a primary key for the relationships.

This template should be paired up with a DB schema generation to keep API and DB in unison. See the hasura tutorial for an example.

A more complex template is hasura-abac.json.jina. This example expects each moddelled attribute to be stereotyped with a data sensitivity. Each sensitivity level will create a set of attributes that a user role can access - I.e. a user can have access to sensitive fields but not highly sensitive.


Django
------

    path: mdg/templates/Django/*

There is a set of templates in this folder which mirrors a complete Django app with a Django Rest Framework API. It reccomended to use the Django project boilerplate like django-admin startproject over the included base files - it does demo well as a one click API but could stop working as new versions of Django are released.
Key templates are the app/* files.

    models.py.jinja 

Designed to be called at package level so each model file becomes a Django app. Abstract base classes are handled and supports one level of inheritance. A sample piece of business logic is included where any object modelled with the 'auditable' stereotype will use django-simple-history to provide audit of who made what change.
