from release_exporter.base import FormatBase
import requests
import json


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
        _json = {"query": "{ repository(owner:\"akshaybabloo\", name:\"gollahalli-com\") { releases{ totalCount } } }"}

        r = requests.post(url=self.api_url, json=_json, headers=self.headers)
        return json.loads(r.text)

    def releases(self):
        _json = {
            "query": """
                query {
                  repository(owner: \"akshaybabloo\", name: \"gollahalli-com\") {
                    releases(first:52, orderBy: {field: CREATED_AT, direction: DESC}){
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
