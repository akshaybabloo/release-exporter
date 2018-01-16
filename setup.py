import codecs
import os
from setuptools import setup

from release_exporter._version import version

here = os.path.abspath(os.path.dirname(__file__)) + os.sep

def get_requirements(*parts):
    return codecs.open(os.path.join(here, *parts), 'r').read().splitlines()


setup(
    name='release-exporter',
    version=version(),
    install_requires=get_requirements('requirements.txt'),
    packages=['tests', 'release_exporter'],
    url='https://github.com/akshaybabloo/release-exporter',
    license='MIT',
    author='Akshay Raj Gollahalli',
    author_email='akshay@gollahalli.com',
    description='Release exporter for GitHub and GitLab.',
    keywords=['changelog', 'releases'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Intended Audience :: Developers',
        'Environment :: Console',
        'Development Status :: 5 - Production/Stable',
        'Topic :: Utilities'
    ],
    entry_points={
        'console_scripts': [
            'rex = release_exporter:main'
        ]
    }
)
