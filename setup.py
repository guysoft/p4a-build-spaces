#!/usr/bin/python3

import os
from setuptools import setup, Extension, Command
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="p4a-build-spaces",
    version="0.1",
    author="p4a build spaces team",
    description="A tool for quickly setting up testing " +
        "and build environments for python-for-android",
    entry_points={
        "console_scripts": ["p4aspaces=p4aspaces.main:main"],
    },
    include_package_data=True,
    package_dir={'':'src'},
    packages=["p4aspaces"] + ["p4aspaces." + p
        for p in setuptools.find_packages("./src/p4aspaces")],
    package_data={
        "p4aspaces":  \
            ["environments/" + env + "/*" for env in os.listdir(
                os.path.join(os.path.dirname(__file__),
                "src", "p4aspaces", "environments"))] +\
            [
                "environments/*.txt",
                "Dockerfile",
            ]
    },
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/JonasT/p4abuildspaces",
    data_files=[("", ["LICENSE.md"])],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
