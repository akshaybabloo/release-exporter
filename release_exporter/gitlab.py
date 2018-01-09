from release_exporter.requests import GitLabRequest
from release_exporter.utils import date_convert


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
        with open('CHANssGELOG.md', 'w') as md_file:
            md_file.writelines(self._converter())

    def _converter(self):
        self.all_content.append(self._header())

        temp = self.releases()
        temp_l = []

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


gitlab_format = GitLabFormat
