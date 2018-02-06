#!/usr/bin/env python

import setuptools
import tivoctl

setuptools.setup(
    name=tivoctl.__title__,
    version=tivoctl.__version__,
    description=tivoctl.__doc__,
    url=tivoctl.__url__,
    author=tivoctl.__author__,
    author_email=tivoctl.__author_email__,
    license=tivoctl.__license__,
    long_description=open("README.md").read(),
    entry_points={
        "console_scripts": ["tivoctl=tivoctl.__main__:main"]
    },
    packages=["tivoctl"],
    install_requires=[],
    extras_require={},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Hom Automation",
    ],
)
