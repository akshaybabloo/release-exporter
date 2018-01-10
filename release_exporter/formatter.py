from release_exporter.requests import GitHubRequest, GitLabRequest
from release_exporter.utils import date_convert, description


class GitHubFormat(GitHubRequest):
    """
    Changelog of GitHub.
    """

    def __init__(self, *args, **kwargs):
        super(GitHubFormat, self).__init__(*args, **kwargs)

        self.compare = 'https://' + self.info.resource + '/' + self.info.owner + '/' + self.info.name + '/compare/'

    def write_json(self):
        """
        Writes down a CHANGELOG.json file.
        """
        pass

    def write_markdown(self):
        """
        Writes down a CHANGELOG.md file.
        """
        with open('CHANGELOG.md', 'w') as md_file:
            md_file.writelines(self._converter())

        print('\n' + 'Done ' + u"\U0001F44D")

    def _converter(self):
        """
        A tuple of formatted tag name, description, created at and the compare links.

        Returns
        -------
        tuple: tuple
            A tuple of list.
        """
        self.all_content.append(self._header())

        temp = self.releases()['data']['repository']['releases']['edges']
        temp_l = []

        description(provider=self.info.resource, repo_name=self.info.name,
                    tags_number=sum(1 for k in temp if k['node']['tag']['name']))

        for edge in temp:
            temp_l.append(edge['node']['tag']['name'])
            self.tag = edge['node']['tag']['name']
            self.content = edge['node']['description'].replace('\r\n', '\n')
            self.date = date_convert(edge['node']['createdAt'])
            self.all_content.append(self._body())

        pair = list(['{}...{}'.format(a, b) for a, b in zip(temp_l, ['master'] + temp_l[:-1])])

        for tags in pair:
            self.all_content.append('[' + tags.split('...')[1] + ']: ' + self.compare + tags + '\n')

        return tuple(self.all_content)


github = GitHubFormat


class GitLabFormat(GitLabRequest):
    """
    Changelog of GitLab.
    """

    def __init__(self, *args, **kwargs):
        super(GitLabFormat, self).__init__(*args, **kwargs)

        self.compare = 'https://' + self.info.resource + '/' + self.info.owner + '/' + self.info.name + '/compare/'

    def write_json(self):
        pass

    def write_markdown(self):
        """
        Writes down a CHANGELOG.md file.
        """
        with open('CHANGELOG.md', 'w') as md_file:
            md_file.writelines(self._converter())

        print('\n' + 'Done ' + u"\U0001F44D")

    def _converter(self):
        """
        A tuple of formatted tag name, description, created at and the compare links.

        Returns
        -------
        tuple: tuple
            A tuple of list.
        """
        self.all_content.append(self._header())

        temp = self.releases()
        temp_l = []

        description(provider=self.info.resource, repo_name=self.info.name,
                    tags_number=sum(1 for k in temp if k['name']))

        for content in temp:
            temp_l.append(content['name'])
            self.tag = content['name']
            self.content = content['release']['description'].replace('\r\n', '\n')
            self.date = date_convert(content['commit']['created_at'])
            self.all_content.append(self._body())

        pair = list(['{}...{}'.format(a, b) for a, b in zip(temp_l, ['master'] + temp_l[:-1])])

        self.all_content.append('\n')

        for tags in pair:
            self.all_content.append('[' + tags.split('...')[1] + ']: ' + self.compare + tags + '\n')

        return tuple(self.all_content)


gitlab = GitLabFormat
