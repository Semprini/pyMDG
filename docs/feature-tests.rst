Test Cases
**********
When generating, a recipie can optionally specify a test package containing test cases to output JSON request and response objects. Specify the package::

   test_package: "{C2E30D48-F8AB-4c6f-9FA3-AFE44653D5EB}"

...and specify the output::

   test_templates:
   - dest: ./build/json{{ins.package.path}}/{{ins.stereotype}}.json
     format: json

In the sample Sparx EA project the SampleIndustry package has the Test child package where the teat modelling can be seen:

.. image:: https://github.com/Semprini/pyMDG/raw/master/docs/_static/image/testmodel.png
