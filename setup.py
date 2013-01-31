import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "spoj",
    version = "0.0.1",
    author = "Nyambayar Turbat",
    author_email = "t.nyambayar@gmail.com",
    description = ("command line tool for spoj.com "),
    license = "BSD",
    keywords = "spoj spoj.com algorithm",
    url = "http://packages.python.org/spoj",
    packages=['spoj', 'tests'],
    long_description=read('README.mk'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
    install_requires=[
        'argparse>=1.2.1',
        'requests>=1.1.0',
        'BeautifulSoup>=3.2.1',
        ]
)
