python -m unittest
python mdg-tool.py generate .\sample_recipes\sparx\config-sparx-django.yaml
python mdg-tool.py generate .\sample_recipes\sparx\config-sparx-docs.yaml
python mdg-tool.py generate .\sample_recipes\sparx\config-sparx-python.yaml
python mdg-tool.py generate .\sample_recipes\sparx\config-sparx-schema.yaml
python mdg-tool.py generate .\sample_recipes\sparx\config-sparx-sqlalchemy.yaml

python mdg-tool.py generate .\sample_recipes\drawio\config-drawio-django.yaml
python mdg-tool.py generate .\sample_recipes\drawio\config-drawio-java.yaml

python mdg-tool.py generate .\sample_recipes\bouml\config-bouml-schema.yaml

python mdg-tool.py dumps .\sample_recipes\bouml\config-bouml-schema.yaml
python mdg-tool.py dumps .\sample_recipes\sparx\config-sparx-schema.yaml
python mdg-tool.py dumps .\sample_recipes\drawio\config-drawio-java.yaml
