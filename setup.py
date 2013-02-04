from setuptools import setup


def get_version():
    """
        get spoj version from "spoj/__init__.py"

        return version number
    """
    for line in open('spoj/__init__.py').readlines():
        if line.startswith('__version__'):
            return eval(line.split('=')[-1])


setup(
    name="spoj",
    version=get_version(),
    author="Nyambayar Turbat",
    author_email="t.nyambayar@gmail.com",
    description="Command line tool for spoj.com",
    license="BSD",
    keywords="spoj, spoj.com, algorithm",  # TODO: improve keywords
    url="http://packages.python.org/spoj", # TODO: change url => github.com/nyamba/spoj ?
    packages=['spoj'],
    include_package_data=True,
    zip_safe=False,
    long_description=open("README.md").read(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "Topic :: Education",
        "License :: OSI Approved :: BSD License",
        "Intended Audience :: Customer Service",
    ],
    install_requires=[
        'setuptools',
        'argparse>=1.2.1',
        'requests>=1.1.0',
        'BeautifulSoup>=3.2.1',
    ],
    entry_points={
        'console_scripts': [
            'spoj = spoj.main:runner',
        ]
    },
)
