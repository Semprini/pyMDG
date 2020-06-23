package my.co.sample.{{ enum.package.parent.name }}.{{ enum.package.name }};


public enum {{ enum.name }}()
{
    {% for value in enum.values %}
    {{ value }}{% if loop.last != True %},{% endif %}{% endfor %}
}
