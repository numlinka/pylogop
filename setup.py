# Licensed under the MIT License.
# logop by numlinka.
# setup

# site
from setuptools import setup


setup(
    name="logop",
    version="1.3.3",
    description = "This is a lightweight and scalable Python logging library.",
    long_description = open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type = "text/markdown",
    author="numlinka",
    author_email="numlinka@163.com",
    url="https://github.com/numlinka/pylogop",
    package_dir={"": "src"},
    packages = ["logop"],
    install_requires=[
        "typex>=0.3.0"
    ],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    license = "MIT",
    keywords = ["sample", "extensible", "logging"]
)
