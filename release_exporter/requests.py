import json

import requests

from release_exporter.base import FormatBase
from release_exporter.utils import get_repo_url_info, multi_key_gitlab


class GitHubRequest(FormatBase):

    def __init__(self, *args, **kwargs):
        super(GitHubRequest, self).__init__(*args, **kwargs)
        self.request_headers = {'Authorization': 'token %s' % self.token}
        self.api_url = 'https://api.github.com/graphql'

        if self.url is not None:
            self.info = get_repo_url_info(self.location, url=self.url)
        else:
            self.info = get_repo_url_info(self.location)

    def _total_number_releases(self):
        _json = {"query": """
            {
              repository(owner: """ + """\"{}\",""".format(self.info.owner) + """ name: """ + """\"{}\")""".format(
            self.info.name) + """ {
                releases {
                  totalCount
                }
              }
            }
        """}

        r = requests.post(url=self.api_url, json=_json, headers=self.request_headers)
        return int(json.loads(r.text)['data']['repository']['releases']['totalCount'])

    def releases(self):
        _json = {
            "query": """
                query {""" +
                     """repository(owner: \"{}\", name: \"{}\") """.format(self.info.owner, self.info.name) + """{
                    releases(""" + """first:{}""".format(self._total_number_releases()) + """, orderBy: {field: CREATED_AT, direction: DESC}){
                      edges{
                        node{
                          name
                          tag{
                            name
                          }
                          description
                          createdAt
                        }
                      }
                    }
                  }
                }
            """
        }

        r = requests.post(url=self.api_url, json=_json, headers=self.request_headers)
        return json.loads(r.text)


class GitLabRequest(FormatBase):

    def __init__(self, *args, **kwargs):
        super(GitLabRequest, self).__init__(*args, **kwargs)
        self.request_headers = {'Private-Token': '%s' % self.token}
        self.api_url = 'https://gitlab.com/api/v4/'

        if self.url is not None:
            self.info = get_repo_url_info(self.location, url=self.url)
        else:
            self.info = get_repo_url_info(self.location)

    def _repo_id(self):
        url = self.api_url + 'projects?search={}'.format(self.info.name)

        r = requests.get(url=url, headers=self.request_headers)
        id_number = json.loads(r.text)

        if len(id_number) > 1:
            print(
                "The search resulted in more that one repository. Please check your repository name and type in it's ID")
            print('ID - Repository Name - Username')

            for content in id_number:
                print('{id} - {repo_name} - {user_name}'.format(id=content['id'], repo_name=content['name'],
                                                                user_name=multi_key_gitlab(content)))

            id_number = input('ID > ')
            return id_number

        return data[0]['id']

    def releases(self):
        url = 'https://gitlab.com/api/v4/projects/{id}/repository/tags'.format(id=self._repo_id())

        r = requests.get(url=url, headers=self.request_headers)
        return json.loads(r.text)
