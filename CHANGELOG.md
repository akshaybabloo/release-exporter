# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- `all` command added - Creates changelog for markdown, rst and json at the same time.
- `deprecate` added in `utils.py`.
- `check_version` added in `utils.py`


### Changed

- `write_*()` -> `write()`. `write_*` will be deprecated in version 1.2
- `requests.py` -> `request.py`
    
## [1.0.6] - 2018-03-01

### Updated

- Blog URL updated
    
## [1.0.5] - 2018-02-21

### Added

- `rest` command added to README.rst
- `rest` command added to cli.py
- `FormatRstBase` added to `base.py`

### Changed

- Header image updated with reStructuredText text

### Fixed

- cli fixed - see #2
    
## [1.0.4] - 2018-01-31

### Removed

- CHANGELOG.rst and README.rst removed
- `pairwise` removed

### Added

- `.tox/*` and `*tests*` to ignore list for codecov
- Codecov and build status badges added
- Tests added -
    - `date_convert`,
    - `multi_key_gitlab`,
    - `description`
    - `base.py`,
    - `version`
    - `test_date_convert_pass2`
    - `test_GitHubRequest_fail`, `test_GitHubRequest_fail_2` and `TestGitHubRequestInit`
    - `TestGitHubRequestFail`
    - `TestGitHubRequest`, `test_GitLabRequest_fail`, `test_GitLabRequest_fail_2`, `TestGitLabRequestInit`, `TestGitLabRequestFail`, `TestGitLabRequest`
    - `test_GitLab_repo_id`
    - `test_get_repo_url_info_fail_2`
    - `test_cli_help`, `test_print_version`
    - `test_markdown_fail`, `test_json_fail`
    - `test_markdown_fail_2`, `test_json_fail_2`
    - `test_markdown_exception`, `test_json_exception`, `test_markdown_fail_3`, `test_json_fail_3`
    - `TestGitHubFormatMarkdown` and `TestGitHubFormatJson`
    - `TestGitLabFormatMarkdown` and `TestGitLabFormatJson`
- `Problems you might encounter` added to `README.md` and typos corrected
- JSON output example added to `README.md`
- `release-exporter.png` added to `README.md`
- `CHANGELOG.json` added
- Usage of `--location` clearly explained.
- Blog URL added to `README.md`
- invalid token added as exception in `exceptions.py`
- Create temp files for testing `get_repo_url_info()`

### Fixed

- `configparser` raises `configparser.DuplicateSectionError` if more than one section is found.

### Changed

- `url` changed in `setup.py`
- `description` now returns a string instead of just printing when the function is called
- `_version.py` -> `version.py`
- `version()` -> `__version__`
- `RequestBase` merged into `FormatBase`
- `sys.exit(1)` -> `raise`
- `main` removed from `__init__.py` and `cli` is used
- `DuplicateSectionError` raised instead of using `print` it
    
## [1.0.3] - 2018-01-16

### Changed
- `v` removed from the version number
- pypandoc usage removed and *.rst format added
- Unwanted encoding removed
    
## [1.0.2] - 2018-01-16

## Added
- Long description and changelog added to setup.py

## Fixed
- Typo
- Exception error type changed to ImportError
    
## [v1.0.1] - 2018-01-16

### Added
- Unreleased tag added to the template and GitHub
- Unreleased tag added to GitHub

### Fixed
- Tag missing in GitHub JSON fixed
- Tag missing in GitLab JSON fixed

## v1.0 - 2018-01-15

Initial release.

[Unreleased]: https://github.com/akshaybabloo/release-exporter/compare/1.0.6...HEAD
[1.0.6]: https://github.com/akshaybabloo/release-exporter/compare/1.0.5...1.0.6
[1.0.5]: https://github.com/akshaybabloo/release-exporter/compare/1.0.4...1.0.5
[1.0.4]: https://github.com/akshaybabloo/release-exporter/compare/1.0.3...1.0.4
[1.0.3]: https://github.com/akshaybabloo/release-exporter/compare/1.0.2...1.0.3
[1.0.2]: https://github.com/akshaybabloo/release-exporter/compare/v1.0.1...1.0.2
[v1.0.1]: https://github.com/akshaybabloo/release-exporter/compare/v1.0...v1.0.1
