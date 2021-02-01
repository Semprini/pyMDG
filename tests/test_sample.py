import unittest
import os


class TestSample_DrawIO_Django(unittest.TestCase):
    def setUp(self):
        self.recipie_path = './sample_recipie' + "/config-drawio-django.yaml"
        os.environ.setdefault("PYMDG_SETTINGS_MODULE", self.recipie_path)

    def test_parse(self):
        from mdg.parse import parse

        model_package, test_cases = parse()
        self.assertEqual("SampleIndustry", model_package.name)
