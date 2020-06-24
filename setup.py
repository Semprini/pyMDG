import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name='pymdg',
    version='0.1a0',
    author='Paul Atkin',
    description='Model driven genration - from UML to Code & Docs',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/semprini/pyMDG',
    packages=setuptools.find_packages(),
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
