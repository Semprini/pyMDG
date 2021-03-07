Diagrams.net Django Tutorial
****************************

To use pyMDG we need to build:
* A UML model
* A generation recipie

Modelling
^^^^^^^^^

pyMDG has a specific UML nomenclature. This needs to be added into diagrams.net by selecting:

File -> Open Library From -> URL and enter::

   https://raw.githubusercontent.com/Semprini/pyMDG/master/mdg/tools/DrawIO%20MDG%20UML%20Library.xml

This will result in the pyMDG library being added to the sidebar:

.. image:: https://raw.githubusercontent.com/Semprini/pyMDG/master/docs/_static/image/MDGUML.JPG

UML packages are set up as Frames in the library. This mimics the hierarchy found in full modelling tools like Sparx. Add 3 nested frames to the canvas and rename each:

* Top level is the name of our business domain/data platform
* 2nd level is the model container (test container can be added later)
* 3rd level is a data domain/app

.. image:: https://raw.githubusercontent.com/Semprini/pyMDG/master/docs/_static/image/Package.JPG

We can then start modelling classes. Each class must have an attribute with {id} except where the {id} is in a parent class.

Drag 2 'Class Basic' objects into the TestDomain package. Rename classes and set the {id} attribute of each class. Drag on an Association and link the classes:

.. image:: https://raw.githubusercontent.com/Semprini/pyMDG/master/docs/_static/image/Class.JPG

There are 5 templates for classes:

* Basic: Vanilla class with attributes
* Abstract: The <<auto>> attribute stereotype is optional.
* Stereotyped: Shows auditable (data platform will track changes) and notifiable (changes will cause events to be sent to the message broker)
* Routable: When events are sent to message broker then routing keys will include attributes with <<routable>> stereotype.

pyMDG supports 2 relation types:

* Association: Forms relations between classes:

   * One to One
   * One to Many
   * Many to One
   * Many to Many

* Generalization: Defines a parent/child inheritance

Export the diagram by File -> Export As -> XML and unselect Compressed

Generate
^^^^^^^^

The recipie tells pyMDG about your model and what files to output. 
This tutorial uses the sample templates and config which you can find in the 
sample_recipie folder from the project on gitgub: https://github.com/Semprini/pyMDG

Recipie - Django
----------------

A complete django app with django rest api can be created from the model.

cd into a new project folder (I called mine django-tut)::

   django-tut> virtualenv venv
   django-tut> pip install pymdg

Copy the following from the github project pyMDG/sample_recipie folder:

* config-drawio-django.yaml
* templates/Django/*

The dir structure now looks like:

.. image:: https://raw.githubusercontent.com/Semprini/pyMDG/master/sample_recipie/images/django-tut-structure.JPG

Edit config-drawio-django.yaml and update the following:

* root_package: QuickStart (matches the top level package)
* model_package: model (matches the middle package)
* source: the path to your saved model file
* templates_folder: ''
* dest_root: ./build

We can now build the project::

   > django-tut> mdg-tool generate .\config-drawio-django.yaml
   Config file loaded: .\config-drawio-django.yaml
   Base Model Package: model
   Generating model output for package /QuickStart/
   Generating model output for package /QuickStart/TestDomain/
   Generating test case output

And then run the generated django app::

   > cd build/QuickStart/
   > pip install -r .\requirements.txt
   > python manage.py makemigrations TestDomain    <- matches the inner package
   Migrations for 'TestDomain':
   TestDomain\migrations\0001_initial.py
    - Create model AnotherClass
    - Create model MyCoolClass

   > python manage.py migrate
   > python manage.py createsuperuser
   > python manage.py runserver

You can now browse to http://127.0.0.1:8000/admin/ and http://127.0.0.1:8000/api/

