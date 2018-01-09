from release_exporter.requests import GitHubRequest


class GitHubFormat(GitHubRequest):
    """
    Changelog of GitHub.
    """

    def __init__(self, *args, **kwargs):
        super(GitHubFormat, self).__init__(*args, **kwargs)

        self.compare = 'https://' + self.info.resource + '/' + self.info.owner + '/' + self.info.name + '/compare/'

    def write_json(self):
        pass



github_format = GitHubFormat
