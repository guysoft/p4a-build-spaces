#!/usr/bin/python3

import os
from setuptools import setup, Extension, Command

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="p4a-build-spaces",
    version="0.1",
    author="p4a build spaces team",
    description="A tool for quickly setting up testing " +
        "and build environments for python-for-android",
    packages=["p4aspaces"],
    entry_points={
        "console_scripts": ["p4aspaces=p4aspaces.p4aspaces"],
    },
    include_package_data=True,
    package_dir={'p4aspaces': ''},
    package_data={
        "p4aspaces":  \
            ["environments/" + env + "/*" for env in os.listdir(
                os.path.join(os.path.dirname(__file__), "environments"))] +\
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
