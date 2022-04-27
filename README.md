# Release Exporter

![Banner](https://raw.githubusercontent.com/akshaybabloo/release-exporter-old/master/release-exporter.png)

**Blog:** [https://www.gollahalli.com/blog/export-your-github-and-gitlab-releases-as-a-changelog/](https://www.gollahalli.com/blog/export-your-github-and-gitlab-releases-as-a-changelog/)

This CLI exports your project releases to a markdown based on [keep a
changelog](http://keepachangelog.com/en/1.0.0/) and
[markdownlint](https://github.com/DavidAnson/markdownlint) and JSON,
it currently supports GitHub and GitLab.

## Install

```bash
pip install release-exporter
```

Or download this repository and type in the following in your
terminal/cmd

```bash
python setup.py install
```

## Usage

In your terminal/cmd, change to the folder where your repository is
located and do the following:

```bash
rex --token <your token> markdown
```

That's it. You should see a `CHANGELOG.md` in your folder.

### Advance Usage

Release exporter has the following options

```bash
Usage: rex [OPTIONS] COMMAND [ARGS]...

Options:
    --token TEXT      Token number if its a private repository.
    --url TEXT        URL of your repository. This is optional if your current
                    directory has .git folder with remote url.
    --location TEXT   Local location of your repository.
    --version
    --universal TEXT  Create a global settings file. Defaults to True.
    --help            Show this message and exit.

Commands:
    all       Creates change log for all formats.
    init      Creates .rex file.
    json      Creates JSON file.
    markdown  Creates markdown file.
    rst       Creates reStructuredText file.
```

If you don't have a repository on your computer, but you still want to
generate a change log you can manually add your repository URL as
follows:

```bash
rex markdown --token <your token> --url <your url>
```

If you have your repository in a different location and you are lazy
(like me) to change into that directory, get the absolute path of your
repository add it to the `--location <location>`.

```bash
rex --token <your token> --location <absolute path>
```

You can also export your releases to JSON file by just replacing
`markdown` with `json`. The output looks something like this:

```json
{
    "repositoryName": "release-exporter",
    "provider": "github.com",
    "owner": "akshaybabloo",
    "repoUrl": "https://github.com/akshaybabloo/release-exporter",
    "totalTags": 2,
    "data": [
        {
            "tagName": "Unreleased",
            "description": "",
            "createdAt": "",
            "compareUrl": "https://github.com/akshaybabloo/release-exporter/compare/1.0.1...HEAD"
        },
        {
            "tagName": "v1.0.1",
            "description": "### Added\n- Unreleased tag added to the template and GitHub\n- Unreleased tag added to GitHub\n\n### Fixed\n- Tag missing in GitHub JSON fixed\n- Tag missing in GitLab JSON fixed",
            "createdAt": "2018-01-16",
            "compareUrl": "https://github.com/akshaybabloo/release-exporter/compare/v1.0...v1.0.1"
        },
        {
            "tagName": "v1.0",
            "description": "Initial release.",
            "createdAt": "2018-01-15",
            "compareUrl": null
        }
    ]
}
```

> **Note:** The `Unreleased` tag is not counted in `totalTags`.

## Problems you might encounter

If you are using `rex` on your repository folder or if you are using
`--location` you might get an error saying that there are duplicate
keys, this is because sometimes the file `.git/config` has more than
one `[remote "origin"]`. In such case, it is best to give the URL of
your repository by giving `--url <repo URL>`.

## Reference

- Markdown logo from [https://github.com/dcurtis/markdown-mark/](https://github.com/dcurtis/markdown-mark/)
