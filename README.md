![Test](https://github.com/Semprini/pyMDG/workflows/Test/badge.svg) ![PyPI](https://github.com/Semprini/pyMDG/workflows/PyPI/badge.svg) [![Documentation Status](https://readthedocs.org/projects/pymdg/badge/?version=latest)](https://pymdg.readthedocs.io/en/latest/?badge=latest)
# pyMDG

## Overview
The problem with most model driven generation is that tools force the modeller to effectively "code up" the output representation of the artifact being generated in an output specific, non-reusable model. It always ends up being simpler just to actually code up the end result.

pyMDGs goal is to use a logical model as the source, then combine with business rules to output physical level artifacts (code, schema, documentation etc). Current version supports Sparx DB (including sqlite which is the '.qea' native file format for Sparx v16+) or diagrams.net XML.

A single logical model is rich enough to generate API schemas, DB schemas, POJOs, Python Data classes etc.

The tool parses your models into generic UML classes (see metamodel below) which are then passed to jinja2 templates for generation.

My current favorite generation recipie is Hasura for a GraphQL API and generating DB migrations via Django. See the tutorial here: [HasuraTutorial](https://pymdg.readthedocs.io/en/latest/tutorial-hasura.html) and check the example config in sample_recipies/sparxdb/config-sparxdb-graphql.yaml

Quickstart and docs can be found here: [readthedocs](https://pymdg.readthedocs.io/en/latest/index.html)

## Test
Testing (powershell):
 > .\test.ps1

Testing (unittest):
 > python -m unittest

## Generate
To generate code call the generate script and pass in the recipe folder. A sample recipe folder is provided in the github repo:
 > python mdg-tool.py generate ./sample_recipe/drawio/config-drawio-django.yaml

Or once installed into site-packages execute:
 > mdg-tool generate <my/config.yaml>

See the sample_recipe configs for examples

## Limitations
Most templates have a limit of single inheritance and no chained inheritance (a is a specialisation of b which is a specialisation of c). The results of this are unknown.

## Sparx EA XMI (versions earlier than V16) Export Process
The UML parser expects a specific package hierarchy, please see the sample EA file.
- In Sparx select the domain root node  (e.g. Model/Sample )
- Select the publish tab at the top
- Select Publish As... from top menu
- Set export type as XMI 2.1
- Optionally select 'Export Diagrams', 'Generate Diagram Images' and PNG format
- Export to folder where you want to generate from


Note: Sparx V16+ does not need to be exported. The parser uses native SQLite file format which is the same schema as database repositories.

## Draw.io Export Process
The UML parser expects a specific package layout which mimics the Sparx hierarchy, please see the sample files.
- In the web editor select Export As -> XML
- Uncheck 'Compressed'

## Wiki documentation upload
If your generation recipe has created a file for your wiki (Confluence) then an uploader utilitity can be used. This assumes that you have done the XMI export from Sparx EA with export diagrams and generate diagram images. 
To generate a confluence token please see: https://confluence.atlassian.com/cloud/api-tokens-938839638.html
> python mdg/confluence.py {your email} {your confluence token} {confluence page id} {path to images} {doc filename}

## Nomenclature:
This diagram shows all the features and how to model in UML
![Nomenclature](https://github.com/Semprini/pyMDG/raw/master/sample_recipes/images/EAID_9100ADB5_EFF8_4ded_BA61_E8564C8134AC.png)

## Sample model
![Sample model](https://github.com/Semprini/pyMDG/raw/master/sample_recipes/images/EAID_96AC850E_2FD0_4e6c_B00E_C030EDA89F42.png)

## Metamodel
This diagram shows the internal classes which are passed to the templates during generation.
![Metamodel](https://raw.githubusercontent.com/Semprini/pyMDG/master/docs/_static/image/metamodel.png)

## Build the docs
Install sphinx
```
 > cd pyMDG
 > sphinx-apidoc -o docs\source mdg
 > cd docs
 > make html
```
