# Release Exporter

[![codecov](https://codecov.io/gh/akshaybabloo/release-exporter/branch/master/graph/badge.svg)](https://codecov.io/gh/akshaybabloo/release-exporter) [![Build Status](https://travis-ci.org/akshaybabloo/release-exporter.svg?branch=master)](https://travis-ci.org/akshaybabloo/release-exporter)

Exports your releases to a markdown based on [keep a changelog](http://keepachangelog.com/en/1.0.0/) and [markdownlint](https://github.com/DavidAnson/markdownlint). This CLI application currently supports GitHub and GitLab.

## Install

```bash
pip install release-exporter
```

Or download this repository and type in the following in your terminal/cmd

```bash
python setup.py install
```

## Usage

In your terminal/cmd, change to the folder where you repository is located and do the following:

```bash
rex --token <your token> markdown
```

That's it. You should see a `CHANGELOG.md` in your folder.


### Advance Usage

Release exporter has the following options

```bash
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
```

If you don't have a repository on your computer but you still want to generate a change log you can manually add your repository URL as following:

```bash
rex markdown --token <your token> --url <your url>
```

If you have your repo in a different location and you are lazy (like me) to change into that directory, get the absolute path of you repository add it to the `--location <location>`.

```bash
rex --token <your token> --location <absoulute path>
```

You can also export your releases to JSON file by just replacing `markdown` with `json`.

### Customising the Output

Coming soon.
