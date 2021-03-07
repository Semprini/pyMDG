![Test](https://github.com/Semprini/pyMDG/workflows/Test/badge.svg) ![PyPI](https://github.com/Semprini/pyMDG/workflows/PyPI/badge.svg) [![Documentation Status](https://readthedocs.org/projects/pymdg/badge/?version=latest)](https://pymdg.readthedocs.io/en/latest/?badge=latest)
# pyMDG

## Overview
Parser and tools to manipulate UML models. Current version supports Sparx EA Generated XMI 2.1 or diagrams.net XML

Used to parse model files to native classes (see metamodel below) which are passed to jinja2 templates for generation of code (POJO, POCO, Django etc), JSON data and HTML documentation.

Quickstart and docs can be found here: [readthedocs](https://pymdg.readthedocs.io/en/latest/index.html)

## Test
Testing:
 > python test.py

To generate code call the generate script and pass in the recipie folder. A sample recipie folder is provided in the github repo:
 > python mdg-tool.py generate ./sample_recipie/config-drawio-django.yaml

Or once installed into site-packages execute:
 > mdg-tool generate <my/config.yaml>

See the sample_recipie configs for examples

## Sparx EA Export Process
The UML parser expects a specific package hierarchy, please see the sample EA file.
- In Sparx select the domain root node  (e.g. Model/Sample )
- Select the publish tab at the top
- Select Publish As... from top menu
- Set export type as XMI 2.1
- Optionally select 'Export Diagrams', 'Generate Diagram Images' and PNG format
- Export to folder where you want to generate from

## Draw.io Export Process
The UML parser expects a specific package layout which mimics the Sparx hierarchy, please see the sample files.
- In the web editor select Export As -> XML
- Uncheck 'Compressed'

## Wiki documentation upload
If your generation recipie has created a file for your wiki (Confluence) then an uploader utilitity can be used. This assumes that you have done the XMI export from Sparx EA with export diagrams and generate diagram images. 
To generate a confluence token please see: https://confluence.atlassian.com/cloud/api-tokens-938839638.html
> python confluence.py {your email} {your confluence token} {confluence page id} {path to images} {doc filename}

## Nomenclature:
This diagram shows all the features and how to model in UML
![Nomenclature](https://github.com/Semprini/pyMDG/raw/master/sample_recipies/images/EAID_9100ADB5_EFF8_4ded_BA61_E8564C8134AC.png)

## Sample model
![Sample model](https://github.com/Semprini/pyMDG/raw/master/sample_recipies/images/EAID_96AC850E_2FD0_4e6c_B00E_C030EDA89F42.png)

## Metamodel
This diagram shows the internal classes which are passed to the templates during generation.
![Metamodel](https://github.com/Semprini/pyMDG/raw/master/sample_recipies/images/EAID_B080F856_9EFB_46f2_8D69_1C79956D714A.png)

## Build the docs
Install sphinx

 > cd pyMDG
 > sphinx-apidoc -o docs\source mdg
 > cd docs
 > make html
