pyMDG's documentation
=====================

Take UML models created in Sparx EA or DrawIO, export and use pyMDG to generate code, schema and documentation. Provided templates generate Django, OpenAPI, Avro, POJOs and more.

Currently used for generating data platforms via UML packages, classes & enumerations.

Quickstart
==========

The github project comes with a sample which can generate a complete data platform.

Generation::

   git clone https://github.com/Semprini/pyMDG
   cd pyMDG
   virtualenv venv
   . venv/bin/activate or .\venv\Scripts\activate
   pip install -r requirements.txt
   python mdg-tool.py generate ./sample_recipe/config-drawio-django.yaml 
   
Run the app::

   cd build/sample_drawio_django/SampleIndustry
   pip install -r requirements.txt
   python manage.py makemigrations TestDomain
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver

And browse to http://127.0.0.1:8000/admin/ or http://127.0.0.1:8000/api/

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. toctree::
   :hidden:
   :maxdepth: 2
   :caption: Tutorials:
   :glob:

   tutorial*


.. toctree::
   :hidden:
   :maxdepth: 2
   :caption: Reference:
   :glob:
   
   metamodel
   recipes
   templates


.. toctree::
   :hidden:
   :maxdepth: 2
   :caption: Code:

   source/modules
