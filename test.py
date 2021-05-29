import unittest
import os
import shutil

recipe_path = './sample_recipes' + "/config-test.yaml"
os.environ.setdefault("PYMDG_SETTINGS_MODULE", recipe_path)

if __name__ == '__main__':

    from mdg.config import settings
    if os.path.exists(settings['dest_root']):
        shutil.rmtree(settings['dest_root'])

    test_loader = unittest.defaultTestLoader
    test_suite = test_loader.discover('mdg')
    test_runner = unittest.TextTestRunner(verbosity=3)
    test_runner.run(test_suite)
