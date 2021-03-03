import unittest
import os
import shutil

recipie_path = './sample_recipie' + "/config-test.yaml"
os.environ.setdefault("PYMDG_SETTINGS_MODULE", recipie_path)

if __name__ == '__main__':

    from mdg.config import settings
    if os.path.exists(settings['dest_root']):
        shutil.rmtree(settings['dest_root'])

    test_loader = unittest.defaultTestLoader
    test_suite = test_loader.discover('.')
    test_runner = unittest.TextTestRunner(verbosity=3)
    test_runner.run(test_suite)
