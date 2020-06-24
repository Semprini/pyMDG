![Test](https://github.com/Semprini/pyMDG/workflows/Test/badge.svg) ![PyPI](https://github.com/Semprini/pyMDG/workflows/PyPI/badge.svg)
# pyMDG

## Overview
Parser and tools to manipulate UML models. Initial version uses Sparx EA Generated XMI 2.1
Can be used to parse XMI file passed to jinja2 templates for generation of code (POJO, POCO, Django etc), JSON data and HTML documentation.

## Test
To generate code a recipie folder is provided:
> python generate.py <recipie folder>

Or once installed into site-packages:
> python
> from pymdg import generator
> generator.parse('{folder}')

The recipie folder must have a config.yaml file which specifies templates and output.

## Export Process
- In Sparx select the domain root node  (e.g. Model/Sample )
- Select the publish tab at the top
- Select Publish As... from top menu
- Set export type as XMI 2.1
- Optionally select 'Export Diagrams', 'Generate Diagram Images' and PNG format
- Export to folder where you want to generate from

## Wiki documentation upload
If your generation recipie has created a file for your wiki (Confluence) then an uploader utilitity can be used. This assumes that you have done the XMI export from Sparx EA with export diagrams and generate diagram images. 
To generate a confluence token please see: https://confluence.atlassian.com/cloud/api-tokens-938839638.html
> python confluence.py {your email} {your confluence token} {confluence page id} {path to images}

## Nomenclature:
This diagram shows all the features and how to model in UML
![Nomenclature](/test_recipie/Images/EAID_9100ADB5_EFF8_4ded_BA61_E8564C8134AC.png)

## Sample model
![Sample model](/test_recipie/Images/EAID_8B1CACEB_2CAB_458e_BED9_DA3ADD6F3F70.png)

## Metamodel
This diagram shows the internal classes which are passed to the templates during generation.
![Metamodel](/test_recipie/Images/EAID_B080F856_9EFB_46f2_8D69_1C79956D714A.png)
