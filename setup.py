from setuptools import setup


setup(**{
    "name": "spoj",
    "version": open("spoj/__init__.py").readlines()[0].split("=")[-1],
    "author": "Nyambayar Turbat",
    "author_email": "t.nyambayar@gmail.com",
    "description": "CLI client for spoj.com",
    "license": "BSD",
    "keywords": "spoj, sphere, online judge, algorithm",
    "url": "http://github.com/nyamba/spoj",
    "packages": ["spoj"],
    "include_package_data": True,
    "zip_safe": False,
    "long_description": open("README.md").read(),
    "classifiers": [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Customer Service",
        "License :: OSI Approved :: BSD License",
        "Topic :: Education",
        "Topic :: Utilities",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python",
    ],
    "install_requires": [
        "setuptools",
        "argparse>=1.2.1",
        "requests>=1.1.0",
    ],
    "entry_points": {
        "console_scripts": [
            "spoj2 = spoj.runner:bootstrap",
        ]
    },
})
