import os

from setuptools import setup

def find_packages(srcdir):
    package_list = []
    badnames=["__pycache__",]
    for root, _, files in os.walk(srcdir):
        if not any(bad in root for bad in badnames):
            if "__init__.py" in files:
                package_list.append( root.replace("/",".").replace("\\",".").strip('.') )
    return package_list

packages = find_packages('.')

setup(name='pymdg',
    version='0.1a0',
    packages=packages,
    install_requires=[
        "lxml",
        "jinja2",
        "pyyaml",
    ],
)
