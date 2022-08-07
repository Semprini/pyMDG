Nomenclature
************

.. image:: https://github.com/Semprini/pyMDG/raw/master/sample_recipes/images/EAID_9100ADB5_EFF8_4ded_BA61_E8564C8134AC.png

pyMDG supports 4 relation types:

* Association: Forms relations between classes:

   * One to One
   * One to Many
   * Many to One
   * Many to Many

* Generalization: Defines a parent/child inheritance. Multi-inheritance in not yet supported.

* Composition: Similar to association but can be used to control generated features. For example, when generating an OpenAPI schema, objects which are part of a composition may not get thier own endpoint.

* Aggregation: Like composition aggregations affect the features of our output. For example, an OpenAPI generation can use aggregations to specifiy when the endpoint is a sub-endpoint I.e. /customer/12/customer_address/1/
