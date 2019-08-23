from setuptools import find_packages, setup

import git_turf.git_turf as git_turf

setup(
    name=git_turf._name,
    version=git_turf._version,
    description=git_turf._description,
    long_description=open("README.rst").read(),
    author=git_turf._author,
    author_email=git_turf._author_email,
    url=git_turf._url,
    license=git_turf._license,
    py_modules=["git_turf"],
    entry_points={"console_scripts": ["git-turf = git_turf.git_turf:main"]},
    packages=find_packages(exclude=("tests", "docs", "misc")),
    test_suite="tests",
)
