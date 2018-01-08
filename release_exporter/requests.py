from release_exporter.base import FormatBase
import requests
import json
from release_exporter.utils import get_repo_url_info


class GitHubRequest(FormatBase):

    def __init__(self, *args, **kwargs):
        super(GitHubRequest, self).__init__(*args, **kwargs)
        self.headers = {'Authorization': 'token %s' % self.token}
        self.api_url = 'https://api.github.com/graphql'

        if self.url is not None:
            self.info = get_repo_url_info(self.location, url=self.url)
        else:
            self.info = get_repo_url_info(self.location)

    def _total_number_releases(self):
        _json = {"query": """
            {
              repository(owner: """ + """\"{}\",""".format(self.info.owner) + """ name: """ + """\"{}\")""".format(self.info.name) + """ {
                releases {
                  totalCount
                }
              }
            }
        """}

        r = requests.post(url=self.api_url, json=_json, headers=self.headers)
        return int(json.loads(r.text)['data']['repository']['releases']['totalCount'])

    def releases(self):
        _json = {
            "query": """
                query {""" +
                  """repository(owner: \"{}\", name: \"{}\") """.format(self.info.owner, self.info.name) + """{
                    releases("""+"""first:{}""".format(self._total_number_releases())+""", orderBy: {field: CREATED_AT, direction: DESC}){
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

        r = requests.post(url=self.api_url, json=_json, headers=self.headers)
        return json.loads(r.text)
