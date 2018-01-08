from release_exporter.requests import GitHubRequest


class GitHubFormat(GitHubRequest):
    """
    Changelog of GitHub.
    """

    def __init__(self, *args, **kwargs):
        super(GitHubFormat, self).__init__(*args, **kwargs)

    def write_json(self):
        pass

    def process(self):
        content = self.releases()
        print(content)


github_format = GitHubFormat
