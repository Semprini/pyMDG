# pyMDG

## Overview
Parser and tools to manipulate UML models. Initial version uses Sparx EA Generated XMI 2.1
Can be used to parse XMI file passed to jinja2 templates for generation of code (POJO, POCO, Django etc), JSON data and HTML documentation.

## Test
To generate code a recipie folder is provided:
> python generate.py <recipie folder>

Or once installed into site-packages:
> python
from pymdg import generator
generator.parse('{folder}')

The recipie folder must have a config.yaml file which specifies templates and output.

## Wiki documentation upload
If your generation recipie has created a file for your wiki (Confluence) then an uploader utilitity can be used. This assumes that you have done the XMI export from Sparx EA with export diagrams and generate diagram images. 
To generate a confluence token please see: https://confluence.atlassian.com/cloud/api-tokens-938839638.html
> python confluence.py {your email} {your confluence token} {confluence page id} {path to images}


## Metamodel:
![GitHub Logo](/test_recipie/Images/EAID_9100ADB5_EFF8_4ded_BA61_E8564C8134AC.png)
