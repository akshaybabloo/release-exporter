import codecs
import os
from setuptools import setup

from release_exporter import __version__

here = os.path.abspath(os.path.dirname(__file__))


try:
    import pypandoc

    long_description = pypandoc.convert(here + 'README.md', 'rst')
    long_description = long_description.replace("\r", "")  # Do not forget this line

    changelog = pypandoc.convert(here + 'CHANGELOG.md', 'rst')
    changelog = changelog.replace('\r', "")
except OSError:
    print("Pandoc not found. Long_description conversion failure.")
    import io

    # pandoc is not installed, fallback to using raw contents
    with io.open(here + 'README.md', encoding="utf-8") as f:
        long_description = f.read()

    with io.open(here + 'CHANGELOG.md', encoding="utf-8") as f:
        changelog = f.read()




def get_requirements(*parts):
    return codecs.open(os.path.join(here, *parts), 'r').read().splitlines()


setup(
    name='release-exporter',
    version=__version__,
    install_requires=get_requirements('requirements.txt'),
    packages=['tests', 'release_exporter'],
    url='https://github.com/akshaybabloo/release-exporter',
    license='MIT',
    author='Akshay Raj Gollahalli',
    author_email='akshay@gollahalli.com',
    description='Release exporter for GitHub and GitLab.',
    long_description= long_description + '\n\n' + changelog,
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
