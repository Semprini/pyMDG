Welcome to pyMDG Documentation
==============================

Take UML models created in Sparx EA or DrawIO and use pyMDG to generate code, schema and documentation. Provided templates generate Django, OpenAPI, Avro, POJOs and more. If you create reusable templates or improve upon the provided ones, please submit them in GitHub.

Currently used for generating data platforms, API & Kafka schema via UML packages, classes & enumerations.

Modelling
=========

pyMDG has a few opinions on the way we data model. This nomenclature enables rule based declaration of things like API endpoints. This can be seen in the nomenclature reference documentation and also see the sample data models in the sample_recipies folder in the Git repo.

Quickstart
==========

The github project comes with sample recipes which can generate a many artifacts including a Django Rest data platform. The generation is definied in recipies, see the sample_recipies or the recipies docs to see how they work.

Generation::

   git clone https://github.com/Semprini/pyMDG
   cd pyMDG
   virtualenv venv
   . venv/bin/activate or .\venv\Scripts\activate
   pip install -r requirements.txt
   python -m mdg.tools.mdg_tool generate ./sample_recipe/drawio/config-drawio-django.yaml 
   
Run the app::

   cd build/sample_drawio_django/SampleIndustry
   pip install -r requirements.txt
   python manage.py makemigrations TestDomain TestDomain2
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver

And browse to http://127.0.0.1:8000/admin/ or http://127.0.0.1:8000/api/

When installed via pip, and you've created your own project, pyMDG provides the mdg-tool command.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. toctree::
   :hidden:
   :maxdepth: 1
   :caption: Features:
   :glob:

   feature-tools
   recipes
   templates
   feature-tests


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
   
   nomenclature
   metamodel


.. toctree::
   :hidden:
   :maxdepth: 2
   :caption: Code:

   source/modules
