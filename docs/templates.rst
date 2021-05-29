Output Templates
================

The project has a set of templates provided in the mdg/templates folders. A template is rendered by specifying it in a recipe and calling mdg-tool generate <recipe file name>.

The recipe will also specify the level. 
If the level is "package" then the template will be called once for each package and subpackage in the UML model.
If the level is "class" then the template will be called once for each class in each package in the UML model.

Passed into the template will be either a "package" or a "cls" argument. The provided argument will conform to the Metamodel.

We can then render almost any artifact.

Here's an example of generating a list of classes in a package::

    {% for cls in package.classes %}
        {{ cls.name }}
    {% endfor %}

With the recipe specifying the above template at package level, we would get a file generated for each UML package containing just the names of the classes in the package
