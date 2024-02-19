Hasura & Django Tutorial
************************

This probably feels like an odd mix. Django is a full ORM and everyone uses Django Rest for an API dont they?

Django and Django Rest Framework do indeed rock, and a great solution when you are providing an API with a known query pattern.

If you have worked on more generic API platforms then you should understand how hard it is to maintain and develop a RESTful API when we start adding things like writable nested fields, an "expand" url paramater or sub-object depth to support multiple ways of consuming the API.
This is where GraphQL excels and specifically Hasura for Model Driven Generation. Like Django, Hasura is opinionated but unlike Django it's opnionated approach can be driven purely by configuration - a perfect case for model driven generation.

Django has a great database migration system, which is driven from python classes. Other options here are Liquibase and Flyway but Django migrations are created from the delta between the python class and the DB so gives the flexibility of being able to support multiple DB back-ends - I often use SQLite on my dev machine for example. I also like the data manipulation ability in Django for support and data fix tasks, plus the admin interface gives a lot of data management capability out of the box.

Here's a component diagram of the solution:

.. image:: https://github.com/Semprini/pyMDG/raw/master/docs/_static/image/hasura_tut_component.png

This tutorial won't cover the data modelling side. The Sparx tutorial will take you through this. In the github repo, the pyMDG/sample_recipes/sparxdb folder has a sample.qea file with a simple data model. The model shows how the default generation templates realize many-to-one and many-to-many relationships. Here's the simple data model:

.. image:: https://github.com/Semprini/pyMDG/raw/master/docs/_static/image/hasura_tut_model.png


Setup
^^^^^

1. Create a new folder for our solution: hasura_tut

2. Spin up Hasura and PostgreSQL
   | Here's a docker compose config. Note all the hard coded passwords which you should never do outside of a tutorial:

      | https://github.com/Semprini/pyMDG/raw/master/docs/tutorials/hasura/docker-compose.yaml

   | Copy the docker compose yaml into our project folder

   | Spin up the environment:

      | docker compose up -d
   
   | Check that you can log in to Hasura and see the DB on http://localhost:8080/ (or whatever server address your docker is on if not localhost)

   | Create a blank database called customer (matching the root package name, snake_cased) on the PostgreSQL. Something like:

.. code-block:: postgresql

      CREATE DATABASE customer
         WITH
         OWNER = postgres
         ENCODING = 'UTF8'
         LC_COLLATE = 'en_US.utf8'
         LC_CTYPE = 'en_US.utf8'
         TABLESPACE = pg_default
         CONNECTION LIMIT = -1
         IS_TEMPLATE = False;

3. Copy the sample sparx model file into our project folder. 

      | https://github.com/Semprini/pyMDG/raw/master/sample_recipes/sparxdb/sample.qea

   | Note this uses a .qea file which is Sparx v16+ format and is actually a SQLite DB. This means we can support larger modelling teams using shared DB repositories by just pointing the config below to the repo DB.

4. Setup the python bits

      | cd hasura_tut
      | virtualenv .venv
      | . ./venv/bin/activate (or .\\.venv\\Scripts\\activate on windows)
      | pip install pymdg django psycopg[binary]
      | mkdir build
      | cd build
      | django-admin startproject Customer
      
   | Note: the Customer name used in startproject comes from the package name in our Sparx model file which is our generation root package.

Create Config File
^^^^^^^^^^^^^^^^^^

1. cd back to hasura_tut folder

2. Create a blank project using pyMDG

      | mdg-tool startproject --source="sqlite:///sample.qea" --parser=sparxdb --model_package="{AEB30CD7-DECA-4310-BFD6-9225F9251D9A}" --default_dialect=django config-hasura_tut.yaml

   | Note: The GUID for the model package can be seen in Sparx by selecting Model->Simple->Customer package in the Browser window, selecting the Start tab at the top, Properties (in All Windows) and Properties, then expand Project in the Properties window.

      | check that the config-hasura_tut.yaml file is now created.

3. Add the hasura config and django models as generation artifacts to automate

      | mdg-tool addtemplate django_model config-hasura_tut.yaml
      | mdg-tool addtemplate hasura config-hasura_tut.yaml

4. Run the generation

      | mdg-tool generate config-hasura_tut.yaml

      | cd ./build/Customer folder
   
   | This folder should now have everything and look like:
   
      | <folder> Customer
      | <folder> Location
      | <folder> PartyRole
      | hasura_metadata.json
      | manage.py

   | The Sparx model has Location and Party Role packages nested under the Customer package, which the template realizes as Django apps. These are the types of design decisions we make when building an automation template.

Migrate the Database
^^^^^^^^^^^^^^^^^^^^

1. Configure the Django project to use the running PostgreSQL

   | Open Customer/settings.py, find the DATABASES dictionary and change it to:

.. code-block:: python

      DATABASES = {
         'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'customer', 
            'USER': 'postgres',
            'PASSWORD': 'mypostgrespassword',
            'HOST': '127.0.0.1', 
            'PORT': '5432',
         }
      }

2. Add the Django apps to the Django project

   | Still in settings.py, find the INSTALLED_APPS dictionary and change it to:

.. code-block:: python

      INSTALLED_APPS = [
         'django.contrib.admin',
         'django.contrib.auth',
         'django.contrib.contenttypes',
         'django.contrib.sessions',
         'django.contrib.messages',
         'django.contrib.staticfiles',
         'Location',
         'PartyRole',
      ]

3. Make the initial migrations for our two added django apps - Location and PartyRole

   | Back in the cmd/shell:

      | python manage.py makemigrations Location PartyRole

4. Apply the migrations to the DB:

      | python manage.py migrate


Apply Hasura Config
^^^^^^^^^^^^^^^^^^^

This is a manual process using the UI in this tutorial, but Hasura does offer an API to automate this process as part of a build pipeline.

1. Log in to Hasura UI
2. Upload config file
3. Use the API

Final Thoughts
^^^^^^^^^^^^^^

The Hasura generation template has a hard coded connection to the PostgreSQL DB container. In the real-world, think about how you would pipeline this with deployment variables. Check out the templates documentation - each template is just a jinja2 file and the sample ones can all be found under mdg/templates/

In larger organisations there will be DBA teams and change control. Hopefully you can see how this workflow can be integrated to a full continuous delivery pipeline. The high level steps could be:

1. Generate sql code for migrations using:

      | python manage.py sqlmigrate Location 0001 >mysqlmigration0001.sql

   | Do the same for PartyRole and submit this as code into your repo

2. Submit the hasura config as code into your repo

3. Write a deployment pipeline to apply the migration script and hasura config via the API

