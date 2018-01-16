Release Exporter
================

Exports your releases to a markdown based on `keep a
changelog <http://keepachangelog.com/en/1.0.0/>`__ and
`markdownlint <https://github.com/DavidAnson/markdownlint>`__. This CLI
application currently supports GitHub and GitLab.

Install
-------

.. code:: cmd

    pip install release-exporter

Or download this repository and type in the following in your
terminal/cmd

.. code:: cmd

    python setup.py install

Usage
-----

In your terminal/cmd, change to the folder where you repository is
located and do the following:

.. code:: cmd

    rex --token <your token> markdown

That's it. You should see a ``CHANGELOG.md`` in your folder.

Advance Usage
~~~~~~~~~~~~~

Release exporter has the following options

.. code:: cmd

    Usage: rex [OPTIONS] COMMAND [ARGS]...

    Options:
      --token TEXT     Token number if its a private repository.
      --url TEXT       URL of your repository. This is optional if your current
                       directory has .git folder with remote url.
      --location TEXT  Local location of your repository.
      --version
      --help           Show this message and exit.

    Commands:
      json      Creates JSON file.
      markdown  Creates markdown file.

If you don't have a repository on your computer but you still want to
generate a change log you can manually add your repository URL as
following:

.. code:: cmd

    rex markdown --token <your token> --url <your url>

if you want to save it in a custom location you can use
``--location <location>``.

You can also export your releases to JSON file by just replacing
``markdown`` with ``json``.

Customising the Output
~~~~~~~~~~~~~~~~~~~~~~

Coming soon.
