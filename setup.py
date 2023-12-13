"""Setuptools for aiocloudlibrary."""
import setuptools

with open("README.md") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aiocloudlibrary",
    author="Geert Meersman",
    author_email="geertmeersman@gmail.com",
    description="Module to communicate to the Cloud Library API",
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/geertmeersman/aiocloudlibrary",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    install_requires=[val.strip() for val in open("requirements.txt")],
    version="v0.1.0",
)
