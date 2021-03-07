from arango_orm import Collection, fields

{% for entity in package.classes %}
class {{ entity.name }}(Collection):
    __collection__ = '{{ entity.name.lower() }}'
    
    {% for attr in entity.attributes %}{% if attr == entity.id_attribute %}_key = fields.{{attr.dest_type}}(required=True)
    
    @property
    def {{ attr.name }}(self):
        return self._key
    
    @{{ attr.name }}.setter
    def {{ attr.name }}(self, value):
        self._key = value
        
    {% else %}{{attr.name}} = fields.{%if attr.classification.__class__.__name__ == "UMLEnumeration"%}String{% else %}{{attr.dest_type}}{% endif %}()
    {% endif %}{% endfor %}
    def __str__(self):
        return "<{{ entity.name }}({})>".format(self._key)    
    
{% endfor %}
