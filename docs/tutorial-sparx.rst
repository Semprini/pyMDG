Sparx EA XMI Tutorial
****************************

This tutorial uses Sparx EA version 16 but any version which can output XMI 2.1 should work. Note, version 16 of Sparx EA changes it's own file format to a SQLite DB with the same schema as the DB based repository so pyMDG will add this as the prefered mode and XMI export will stop having features added.

To use pyMDG we need to build:

* A UML data model
* A generation recipe

Data Modelling
^^^^^^^^^^^^^^

pyMDG has a specific UML nomenclature, expects Sparx EA project to have a package as a "Model Root" and an optional separate package root for test objects. pyMDG is a little opinionated in how we should create logical data models - We should always use plain language and not use any implementation specific details like snake_case. Let the generation handle realizing the physical models based on the rules in our generation templates.

1. Create the project

   In Sparx EA, create a new project called tutorial1. This will add a default "Model" package as a start.

   Right click on the "Model" package and select Add View...

   This will show the "Add Package" window. Name the package "Tutorial Data Model" and select the "Create Diagram" option. Click Ok.

   This will show the "New Diagram" window. In the "Select From" panel selct "UML Structural" and in the "Diagram Types" panel select "Class" and hit Ok. The diagram name will pickup the package name.

   Open up the diagram and now we model.

2. Data Model

   We'll model a starndard party / party role for the customer role in this tutorial. Drag a Class object into the diagram, name it Party and set it as Abstract.

   Add an integer attribute to Party called id and set "is ID" to true.

   Add a new Class object onto the diagram, name it Individual and add a Generalization from Individual to Party. 
   
   Add "First Name" and "Last Name" attributes to the Individual object. Make the attribute type of both "string"

   Add a new Class object onto the diagram, name it Organisation and add "Name" string attribute and a Generalization from Organisation to Party. 
   
   Next we add the "Party Role" abstract class with an integer Id field. We also add a "Customer" object with a "Name" string attribute and a Generalization relationaship fom Customer to Party Role.

   To relate party role to party we add an Association from Party Role to Party. In the association properties, set the direction to "Source -> Destination" this is to make is obvious who owns the relationship which is important when generating code.

   A party can play many roles so under Properties we go to Source and set Multiplicity to 0..* and under Target we set 0..1. It's just a personal preference so you may want the Target to not be optional and so use a Multiplicity of 1.

   The last object to put on the diagram is an Enumeration. Name it "Customer Types" and add these attributes: Retail, High Value, Corporate, SME.

   To use our enumeration we add an attribute to the Customer object called "Customer Type" and under the Type dropdown choose "Select Type..." and browse to the Customer Types enumeration.

   Your model should now look like:

.. image:: https://github.com/Semprini/pyMDG/raw/master/docs/_static/image/sparx_tut_datamodel.png

3. Exporting

   In the Sparx EA Browser window, single click on the "Tutorial Data Model" package.

   In the top menu bar select "Publish" and choose "Publish As...". I prefer this to "Export Package" as it gives the option to export diagram images if we're generating documentation.

   In the Publish Model Package window, make sure the Package is set to Tutorial Data Model, set an output file as tutorial1.xmi, choose UML 2.3 (XMI 2.1) and hit Export. 

   You can open the exported file in a text editor like Notepad++ and the 2nd line should say: 
   ``<xmi:XMI xmlns:xmi="http://schema.omg.org/spec/XMI/2.1" xmi:version="2.1" xmlns:uml="http://www.omg.org/spec/UML/20090901">``
