import codecs
import os
from setuptools import setup

from release_exporter.version import __version__

here = os.path.abspath(os.path.dirname(__file__)) + os.sep


def get_requirements(*parts):
    return codecs.open(os.path.join(here, *parts), "r").read().splitlines()


setup(
    name="release-exporter",
    version=__version__,
    install_requires=get_requirements("requirements.txt"),
    packages=["tests", "release_exporter"],
    url="https://www.gollahalli.com/blog/export-your-github-and-gitlab-releases-as-a-changelog/",
    license="MIT",
    author="Akshay Raj Gollahalli",
    author_email="akshay@gollahalli.com",
    description="Release exporter for GitHub and GitLab.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    keywords=["changelog", "releases"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Intended Audience :: Developers",
        "Environment :: Console",
        "Development Status :: 5 - Production/Stable",
        "Topic :: Utilities",
    ],
    entry_points={"console_scripts": ["rex = release_exporter.cli:main"]},
)
