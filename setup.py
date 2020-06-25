import os
import setuptools

def find_packages(srcdir):
    package_list = []
    badnames=["__pycache__", "venv", ]
    for root, dirs, files in os.walk(srcdir):
        if not any(bad in root for bad in badnames):
            if "__init__.py" in files:
                package_list.append( root.replace("/",".").replace("\\",".").strip('.') )
    return package_list

pyxmi_packages = find_packages('./mdg')

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name='pymdg',
    version='0.1a3',
    author='Paul Atkin',
    description='Model driven genration - from UML to Code & Docs',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/semprini/pyMDG',
    packages=["mdg",] + pyxmi_packages,
    entry_points={
        'console_scripts': [
            'mdg_generate=mdg.generate:main',
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "lxml",
        "jinja2",
        "pyyaml",
    ],
    python_requires='>=3.5',
)
