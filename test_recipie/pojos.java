package nz.co.genesis_energy.{{ cls.package.parent.name }}.{{ cls.package.name }};

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.Id;

@Entity
public class {{ cls.name }}()
{
    {% for attr in cls.attributes %}{% if attr.is_id %}
    @Id{% endif %}
    @Column (name = "{{attr.name}}"{% if attr.dest_type == 'String' %}, length={{attr.length}}{% endif %})
    private {{attr.dest_type}} {{attr.name}};
    {% endfor %}{% for assoc in cls.associations_from %}
    @Expandable (name = "{{assoc.source_name}}", expandableClass = {{ assoc.dest.name }}.class)
    private {{assoc.dest.name}} {{assoc.source_name}};
    {% endfor %}{% for attr in cls.attributes %}
    public {{ attr.dest_type }} get{{ attr.name }}() {
        return {{ attr.name }};
    }

    public void set{{ attr.name }}({{ attr.dest_type }} {{ attr.name }}) {
        this.{{ attr.name }} = {{ attr.name }};
    }    
    {% endfor %}
}
