MDG Tool
********
pyMDG installs an execuitable called mdg-tool. We run the tool to generate artifacts but it can also validate and dump to JSON. A command to start a new project is uncompleted.

Usage::

   mdg-tool [-h] [--verbose] {generate,validate,dumps,startproject}

Generate
========
Runs the model generation based on provided recipie

Usage::

   mdg-tool generate [-h] recipe_path

Validate
========
Parses the source model specified in the recipie and checks:

* Does each concrete object have an Id field
* Both a parent and specialization should not have an Id
* Each 'auto' stereotyped attribute is either int or bigint 

Usage::

   mdg-tool validate [-h] recipe_path

JSON Dumps
==========
This command will parse the source model from the provided recipie and dump the internal representation as JSON.

Usage::

   mdg-tool dumps [-h] recipe_path

