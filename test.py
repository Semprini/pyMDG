import unittest
import os

recipie_path = './sample_recipie' + "/config-drawio-django.yaml"
os.environ.setdefault("PYMDG_SETTINGS_MODULE", recipie_path)

if __name__ == '__main__':
    test_loader = unittest.defaultTestLoader
    test_suite = test_loader.discover('.')
    test_runner = unittest.TextTestRunner()
    test_runner.run(test_suite)
