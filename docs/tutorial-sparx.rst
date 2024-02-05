Sparx EA XMI Tutorial
*********************

This tutorial uses Sparx EA version 16 but any version which can output XMI 2.1 should work. Note, version 16 of Sparx EA changes it's internal file format to a SQLite DB with the same schema as the DB based repository so pyMDG will add this as the prefered mode and XMI export will stop having features added.

To use pyMDG we need to build:

* A UML data model
* A generation recipe

We start by creating a folder somewhere called tutorial1.

Data Modelling
^^^^^^^^^^^^^^

pyMDG has a specific UML nomenclature, expects Sparx EA project to have a package as a "Model Root" and an optional separate package root for test objects. pyMDG is a little opinionated in how we should create logical data models - We should always use plain language and not use any implementation specific details like snake_case. Let the generation handle realizing the physical models based on the rules in our generation templates.

1. Create the project

   | In Sparx EA, create a new project called tutorial1 in the tutorial1 folder. This will add a default "Model" package as a start.
   | Right click on the "Model" package and select Add View...
   | This will show the "Add Package" window. Name the package "Tutorial Data Model" and select the "Create Diagram" option. Click Ok.
   | This will show the "New Diagram" window. In the "Select From" panel selct "UML Structural" and in the "Diagram Types" panel select "Class" and hit Ok. The diagram name will pickup the package name.
   | Open up the diagram and now we model.

2. Data Model

   | We'll model a starndard party / party role for the customer role in this tutorial. Drag a Class object into the diagram, name it Party and set it as Abstract.
   | Add an integer attribute to Party called id and set "is ID" to true.
   | Add a new Class object onto the diagram, name it Individual and add a Generalization from Individual to Party. 
   | Add "First Name" and "Last Name" attributes to the Individual object. Make the attribute type of both "string"
   | Add a new Class object onto the diagram, name it Organisation and add "Name" string attribute and a Generalization from Organisation to Party. 
   | Next we add the "Party Role" abstract class with an integer Id field. We also add a "Customer" object with a "Name" string attribute and a Generalization relationaship fom Customer to Party Role.
   | To relate party role to party we add an Association from Party Role to Party. In the association properties, set the direction to "Source -> Destination" this is to make is obvious who owns the relationship which is important when generating code.
   | A party can play many roles so under Properties we go to Source and set Multiplicity to 0..* and under Target we set 0..1. It's just a personal preference so you may want the Target to not be optional and so use a Multiplicity of 1.
   | The last object to put on the diagram is an Enumeration. Name it "Customer Types" and add these attributes: Retail, High Value, Corporate, SME.
   | To use our enumeration we add an attribute to the Customer object called "Customer Type" and under the Type dropdown choose "Select Type..." and browse to the Customer Types enumeration.
   | Your project should now look like:

.. image:: https://github.com/Semprini/pyMDG/raw/master/docs/_static/image/sparx_tut_datamodel.png

3. Exporting

   | In the Sparx EA Browser window, single click on the "Tutorial Data Model" package.
   | In the top menu bar select "Publish" and choose "Publish As...". I prefer this to "Export Package" as it gives the option to export diagram images if we're generating documentation.
   | In the Publish Model Package window, make sure the Package is set to Tutorial Data Model, set an output file as tutorial1.xmi in the tutorial1 folder you created earlier, choose UML 2.1 (XMI 2.1) and hit Export. 
   | You can open the exported file in a text editor like Notepad++ and the 2nd line should say: 
   | ``<xmi:XMI xmlns:xmi="http://schema.omg.org/spec/XMI/2.1" xmi:version="2.1" xmlns:uml="http://schema.omg.org/spec/UML/2.1">``


My generated XMI file can be found here: https://raw.githubusercontent.com/Semprini/pyMDG/master/docs/tutorials/sparx/tutorial1.xmi

Generation
^^^^^^^^^^

We can generate many things from our UML declaration. Today I feel the need to generate an OpenAPI and an AVRO schema. We need to tell pyMDG where our source file is, what some of our preferences are and how our Sparx project is structured. We do this in a recipe file.

pyMDG parses the XMI into the internal classes shown in the metamodel section of the docs. It then uses a Jinja2 template for each of the artifacts it needs to generate. pyMDG comes with some templates to get you started - the OpenAPI template can be found in ``mdg/templates/Schema/openapi.yaml.jinja`` and defines GET endpoints for each non-abstract object which must have an Id field (in our case the Id fields for Individual, Organisation and Customer are inherited from an abstract through the generalization associations).

1. Recipie

   | Our first step is to create a file in our tutorial1 folder called schemagen.yaml.
   | We then add info on how our project is set up::

   | root_package: Tutorial Data Model
   | model_package: Tutorial Data Model
   | source: ./tutorial1.xmi
   | parser: sparx

   | Next we add the generation type and where to find our jinja2 templates to the yml::

      | dest_root: ./build
      | templates_folder: ./mdg/templates
      | default_dialect: default

   | Lastly we add a list of the artifacts we want to generate::

      | generation_artifacts:
      | # Avro Schema
      | - dest: "avro/{{cls.package.name}}.{{ cls.name }}.avsc"
      |   level: class
      |   source: "Schema/avro.avsc.jinja"
      | # OpenAPI Schema
      | - dest: "openapi/{{ package.name }}.yaml"
      |   level: package
      |   source: Schema/openapi.yaml.jinja

   | Each list item needs to specify:
   
   * Which Jinja2 template we want to use which will add to the path specified in "templates_folder" but also look through the internal pyMDG templates.
   * A level which specifies if we want the template run for each class or for each package. I want to generate an avsc file per UML class object and an open api yaml file for the package.
   * Where we want to place the resulting artifact. We can use a jinja2 method to include our model structure in the filenames. If the level is class, the "cls" object is passed here and if the level is package then the "package" object is provided. Again see the meta model for what the fields are.

My complete recipe file can be found here: https://github.com/Semprini/pyMDG/raw/master/docs/tutorials/sparx/schemagen.yaml

2. Generation

   | Next we open a CMD prompt and cd into tutorial1
   | I always use a virtual environment so enter::
      
      | virtualenv venv
      | .\\venv\\Scripts\\activate

   | Install pyMDG::

      | pip install pymdg

   | And finally run the generation::

      | mdg-tool generate .\\schemagen.yaml

      | 2022-08-07 20:08:36,476 | mdg.config | INFO | Config file loaded: .\schemagen.yaml
      | 2022-08-07 20:08:36,722 | mdg.parse.sparx_xmi | INFO | Parsing models
      | 2022-08-07 20:08:36,724 | mdg.parse | INFO | Base Model Package: Tutorial Data Model
      | 2022-08-07 20:08:36,724 | mdg.generate.render | INFO | Generating model output for package /Tutorial Data Model/

3. Bask in our own pure awesomeness

   | We should find a build folder created and inside are 2 directories: openapi and avro with our generated artifacts.
   | Copy the openapi file contents and paste into https://editor.swagger.io/
   | You should be able to see the design decisions around endpoints only for non-abstract classes and to have definitions for lists, simple objects and full objects (the difference between simple and full is the inclusion of nested basic objects - see PartyRole for example). 
