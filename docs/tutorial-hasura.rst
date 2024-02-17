Hasura & Django Tutorial
************************

This probably feels like an odd mix. Django is a full ORM and everyone uses Django Rest for an API dont they?

Django and Django Rest Framework do indeed rock, and a great solution when you are providing an API with a known query pattern.

If you have worked on more generic API platforms then you should understand how hard it is to maintain and develop a RESTful API when we start adding things like writable nested fields or sub-object depth to support multiple ways of consuming the API.
This is where GraphQL excels and specifically Hasura for Model Driven Generation. Like Django, Hasura is opinionated but unlike Django it's opnionated approach can be driven purely by configuration - a perfect case for model driven generation.

Django has a great database migration system, which is driven from python classes. Other options here are Liquibase and Flyway but Django migrations are created from the delta between the python class and the DB so gives the flexibility of being able to support multiple DB back-ends - I often use SQLite on my dev machine for example. I also like the data manipulation ability in Django for support and data fix tasks, plus the admin interface gives a lot of data management capability out of the box.

Here's a component diagram of the solution:

.. image:: https://github.com/Semprini/pyMDG/raw/master/docs/_static/image/hasura_tut_component.png

This tutorial won't cover the data modelling side. The Sparx tutorial will take you through this. In the github repo, the pyMDG/sample_recipes/sparxdb folder has a sample.qea file with a simple data model. The model shows how the default generation templates realize many-to-one and many-to-many relationships. Here's the simple data model:

.. image:: https://github.com/Semprini/pyMDG/raw/master/docs/_static/image/hasura_tut_model.png


Generation
^^^^^^^^^^

TBD
