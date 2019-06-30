package nz.co.genesis_energy.{{ enum.package.parent.name }}.{{ enum.package.name }};


public enum {{ enum.name }}()
{
    {% for value in enum.values %}
    {{ value }}{% if loop.last != True %},{% endif %}{% endfor %}
}
