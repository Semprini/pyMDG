![Test](https://github.com/Semprini/pyMDG/workflows/Test/badge.svg) ![PyPI](https://github.com/Semprini/pyMDG/workflows/PyPI/badge.svg)
# pyMDG

## Overview
Parser and tools to manipulate UML models. Initial version uses Sparx EA Generated XMI 2.1
Can be used to parse XMI file passed to jinja2 templates for generation of code (POJO, POCO, Django etc), JSON data and HTML documentation.

## Test
Standard testing:
 > python -m unittest

To generate code call the generate script and pass in the recipie folder. A sample recipie folder is provided in the github repo:
 > python mdg/generate.py sample_recipie

Or once installed into site-packages via 'pip install pymdg', an executable is provided:
 > cd /my/recipie/folder

And execute:
 > mdg_generate

The recipie folder must have a config.yaml file which specifies templates and output. See the sample config for examples

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
![Nomenclature](https://raw.githubusercontent.com/Semprini/pyMDG/master/sample_recipie/images/EAID_9100ADB5_EFF8_4ded_BA61_E8564C8134AC.png)

## Sample model
![Sample model](https://raw.githubusercontent.com/Semprini/pyMDG/master/sample_recipie/images/EAID_96AC850E_2FD0_4e6c_B00E_C030EDA89F42.png)

## Metamodel
This diagram shows the internal classes which are passed to the templates during generation.
![Metamodel](https://raw.githubusercontent.com/Semprini/pyMDG/master/sample_recipie/images/EAID_B080F856_9EFB_46f2_8D69_1C79956D714A.png)
