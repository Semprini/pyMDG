pyMDG's documentation
=====================

pyMDG is a library to allow you to create UML and other models and generate code and documentation. pyMDG currently supports 2 modelling tools: diagrams.net (drawio) and Sparx EA.

Currently used for data systems so supports class diagrams.

Quickstart
==========

The github project comes with a sample which can generate a complete data platform.

Generation::

   git clone https://github.com/Semprini/pyMDG
   cd pyMDG
   virtualenv venv
   . venv/bin/activate or .\venv\Scripts\activate
   pip install -r requirements.txt
   python mdg-tool.py generate ./sample_recipie/config-drawio-django.yaml 
   
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
   templates


.. toctree::
   :hidden:
   :maxdepth: 2
   :caption: Code:

   source/modules
