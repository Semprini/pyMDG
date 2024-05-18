Metamodel
=========

When pyMDG parses the source model file it parses into specific python classes.

.. image:: https://raw.githubusercontent.com/Semprini/pyMDG/master/docs/_static/image/metamodel.png

This will form a hierarchy which looks like::

    UMLPackage: my model package
        UMLPackage: sub package 1
            classes:
                UMLClass: my class 1
                    attributes:
                        UMLAttribute: my attribute 1
                        UMLAttribute: my attribute 2
                UMLClass: my class 2
                ...
        UMLPackage: sub package 2
        ...

The your projects config file you specify the level of the hierarchy to provide to
the template rendering engine. There are 3 levels of rendering templates - root, package and class. 

See Templates page for details on using the parsed classes