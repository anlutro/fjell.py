#!/usr/bin/env python

import os
import setuptools

# allow setup.py to be ran from anywhere
os.chdir(os.path.dirname(os.path.abspath(__file__)))

setuptools.setup(
    name="fjell",
    version="0.1.1",
    license="MIT",
    description="A web framework.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Andreas Lutro",
    author_email="anlutro@gmail.com",
    url="https://github.com/anlutro/fjell.py",
    packages=setuptools.find_packages(include=("fjell", "fjell.*")),
    install_requires=[
        "diay>=0.1.3",
        "werkzeug>=0.12",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    keywords=["web", "framework"],
)
