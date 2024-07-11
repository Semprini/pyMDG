python -m unittest; if ($LastExitCode -ne 0) { throw "Failed unittest" }
python mdg-tool.py generate .\sample_recipes\sparx\config-sparx-django.yaml; if ($LastExitCode -ne 0) { throw "Failed config-sparx-django.yaml" }
# python mdg-tool.py generate .\sample_recipes\sparx\config-sparx-docs.yaml
# python mdg-tool.py generate .\sample_recipes\sparx\config-sparx-python.yaml
# python mdg-tool.py generate .\sample_recipes\sparx\config-sparx-schema.yaml
# python mdg-tool.py generate .\sample_recipes\sparx\config-sparx-sqlalchemy.yaml

# python mdg-tool.py generate .\sample_recipes\drawio\config-drawio-django.yaml
# python mdg-tool.py generate .\sample_recipes\drawio\config-drawio-java.yaml
python mdg-tool.py dumps .\sample_recipes\drawio\config-drawio-java.yaml; if ($LastExitCode -ne 0) { throw "Failed config-drawio-java.yaml" }

# python mdg-tool.py generate .\sample_recipes\bouml\config-bouml-schema.yaml
# python mdg-tool.py dumps .\sample_recipes\bouml\config-bouml-schema.yaml

python mdg-tool.py dumps .\sample_recipes\sparxdb\config-sparxdb-graphql.yaml; if ($LastExitCode -ne 0) { throw "Failed config-sparxdb-graphql.yaml" }

