"""
VoltaHDL setup module

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='VoltaHDL',
    version='0.1.dev0',
    description='A hardware description language (HDL) for circuits',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/craigjb/voltahdl',
    author='Craig Bishop',
    author_email='craig@craigjb.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Manufacturing',
        'Intended Audience :: Other Audience',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='hdl circuit pcb',
    packages=find_packages(exclude=['docs', 'tests']),
    install_requires=[
        'pint==0.8.1',
        'matplotlib==2.2.3',
        'numpy==1.15.0'
    ],
    # extras_require={
    #   'dev': ['check-manifest'],
    #   'test': ['coverage'],
    # },
)
