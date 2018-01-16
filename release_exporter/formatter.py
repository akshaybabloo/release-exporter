import json

from release_exporter.requests import GitHubRequest, GitLabRequest
from release_exporter.utils import date_convert, description


class GitHubFormat(GitHubRequest):
    """
    Changelog of GitHub.
    """

    def __init__(self, *args, **kwargs):
        super(GitHubFormat, self).__init__(*args, **kwargs)

        self.compare_url = 'https://' + self.info.resource + '/' + self.info.owner + '/' + self.info.name + '/compare/'

    def write_json(self):
        """
        Writes down a CHANGELOG.json file.
        """

        self._converter()

        with open(self.file_name + '.' + self.file_type, 'w') as json_file:
            json.dump(self._dict_repo_template(), json_file, indent=4)

        print('\n' + 'Done ' + u"\U0001F44D")

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

        temp = self.releases()['data']['repository']['releases']['edges']
        temp_l = []

        self.total_number_tags = sum(1 for k in temp if k['node']['tag']['name'])

        description(provider=self.info.resource, repo_name=self.info.name, tags_number=self.total_number_tags)

        if self.file_type == 'markdown':

            self.all_content.append(self._header())

            for count, edge in enumerate(temp):
                self.iter_count = count
                temp_l.append(edge['node']['tag']['name'])
                self.tag_name = edge['node']['tag']['name']
                self.description = edge['node']['description'].replace('\r\n', '\n')
                self.date = date_convert(edge['node']['createdAt'])
                self.all_content.append(self._body())

            pair = list(['{}...{}'.format(a, b) for a, b in zip(temp_l, ['HEAD'] + temp_l[:-1])])

            for count, tags in enumerate(pair):
                if count < 1:
                    self.all_content.append('[Unreleased]: ' + self.compare_url + tags + '\n')
                else:
                    self.all_content.append('[' + tags.split('...')[1] + ']: ' + self.compare_url + tags + '\n')

            return tuple(self.all_content)

        elif self.file_type == 'json':

            temp_l2 = []
            tag_comp_url_temp = []
            self.list_descriptions.insert(0, self._dict_data_template(tag_name='Unreleased', description='', date=''))

            for count, edge in enumerate(temp):
                self.iter_count = count
                temp_l2.append(edge['node']['tag']['name'])

                self.list_descriptions.append(self._dict_data_template(tag_name=edge['node']['tag']['name'],
                                                                       description=edge['node'][
                                                                           'description'].replace('\r\n',
                                                                                                  '\n'),
                                                                       date=date_convert(
                                                                           edge['node']['createdAt'])))

            pair = list(['{}...{}'.format(a, b) for a, b in zip(temp_l2, ['HEAD'] + temp_l2[:-1])])

            for tags in pair:
                tag_comp_url_temp.append(self.compare_url + tags)

            for count, urls in enumerate(tag_comp_url_temp):
                self.list_descriptions[count]['compareUrl'] = urls


github = GitHubFormat


class GitLabFormat(GitLabRequest):
    """
    Changelog of GitLab.
    """

    def __init__(self, *args, **kwargs):
        super(GitLabFormat, self).__init__(*args, **kwargs)

        self.compare_url = 'https://' + self.info.resource + '/' + self.info.owner + '/' + self.info.name + '/compare/'

    def write_json(self):
        self._converter()

        with open(self.file_name + '.' + self.file_type, 'w') as json_file:
            json.dump(self._dict_repo_template(), json_file, indent=4)

        print('\n' + 'Done ' + u"\U0001F44D")

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

        temp = self.releases()
        temp_l = []

        self.total_number_tags = sum(1 for k in temp if k['name'])

        description(provider=self.info.resource, repo_name=self.info.name, tags_number=self.total_number_tags)

        if self.file_type == 'markdown':

            self.all_content.append(self._header())

            for count, content in enumerate(temp):
                self.iter_count = count
                temp_l.append(content['name'])
                self.tag_name = content['name']
                self.description = content['release']['description'].replace('\r\n', '\n')
                self.date = date_convert(content['commit']['created_at'])
                self.all_content.append(self._body())

            pair = list(['{}...{}'.format(a, b) for a, b in zip(temp_l, ['HEAD'] + temp_l[:-1])])

            self.all_content.append('\n')

            for count, tags in enumerate(pair):
                if count < 1:
                    self.all_content.append('[Unreleased]: ' + self.compare_url + tags + '\n')
                else:
                    self.all_content.append('[' + tags.split('...')[1] + ']: ' + self.compare_url + tags + '\n')

            return tuple(self.all_content)

        elif self.file_type == 'json':

            temp_l2 = []
            tag_comp_url_temp = []

            for count, content in enumerate(temp):
                self.iter_count = count
                temp_l2.append(content['name'])

                self.list_descriptions.append(self._dict_data_template(tag_name=content['name'],
                                                                       description=content['release'][
                                                                           'description'].replace('\r\n', '\n'),
                                                                       date=date_convert(
                                                                           content['commit']['created_at'])))

            pair = list(['{}...{}'.format(a, b) for a, b in zip(temp_l2, ['master'] + temp_l2[:-1])])

            for tags in pair:
                tag_comp_url_temp.append(self.compare_url + tags)

            for count, urls in enumerate(tag_comp_url_temp):
                if count < self.total_number_tags - 1:
                    self.list_descriptions[count]['compareUrl'] = urls


gitlab = GitLabFormat
