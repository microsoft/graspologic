import os
import sys
import re
from setuptools import setup, find_packages

# Exit if python version is too low.
MINIMUM_PYTHON_VERSION = 3, 6  # Minimum of Python 3.6
if sys.version_info < MINIMUM_PYTHON_VERSION:
    major, minor = MINIMUM_PYTHON_VERSION
    sys.exit(f"Python {major}.{minor}+ is required.")

PACKAGE_NAME = "graspy"
DESCRIPTION = "A set of python modules for graph statistics"
with open("README.md", "r") as f:
    LONG_DESCRIPTION = f.read()
AUTHOR = ("Eric Bridgeford, Jaewon Chung, Benjamin Pedigo, Bijan Varjavand",)
AUTHOR_EMAIL = "j1c@jhu.edu"
URL = "https://github.com/neurodata/graspy"
REQUIRED_PACKAGES = [
    "networkx>=2.1",
    "numpy>=1.8.1",
    "scikit-learn>=0.19.1",
    "scipy>=1.1.0",
    "seaborn>=0.9.0",
    "matplotlib>=3.0.0,<=3.3.0",
    "hyppo>=0.1.3",
]

with open("graspy/__init__.py") as f:
    VERSION = re.search(r'__version__ = "(.*?)"', f.read()).group(1)

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    install_requires=REQUIRED_PACKAGES,
    url=URL,
    license="Apache License 2.0",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Mathematics",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(),
    include_package_data=True,
)
