import json

import requests

from release_exporter.base import FormatBase
from release_exporter.exceptions import InvalidToken
from release_exporter.utils import get_repo_url_info, multi_key_gitlab


class GitHubRequest(FormatBase):
    """
    GitHub request base.
    """

    def __init__(self, *args, **kwargs):
        super(GitHubRequest, self).__init__(*args, **kwargs)
        self.request_headers = {"Authorization": "token %s" % self.token}
        self.api_url = "https://api.github.com/graphql"

        if self.token is None:
            raise InvalidToken(
                "Oops! GitHub requires you to generate a private token to get the details. See "
                "https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/ "
                "for more information."
            )

        if self.repo_url is not None:
            self.info = get_repo_url_info(self.location, repo_url=self.repo_url)
        else:
            self.info = get_repo_url_info(self.location)

    def _total_number_releases(self):
        """
        Queries total number of releases.

        :returns: Number of releases.
        :rtype: int
        """
        _json = {
            "query": f"""
            {{
              repository(owner: \"{self.info.owner}\", name: \"{self.info.name}\") {{
                releases {{
                  totalCount
                }}
              }}
            }}
        """
        }

        r = requests.post(url=self.api_url, json=_json, headers=self.request_headers)

        try:
            response_data = r.json()
        except json.JSONDecodeError:
            raise requests.HTTPError(f"Invalid JSON response: {r.text}")

        if r.status_code >= 400:
            raise requests.HTTPError(f"Request failed with status code {r.status_code}: {r.text}")

        if "errors" in response_data:
            error_messages = [error.get("message", "Unknown error") for error in response_data["errors"]]
            raise ValueError(f"GraphQL query failed with errors: {', '.join(error_messages)}")

        try:
            return int(response_data["data"]["repository"]["releases"]["totalCount"])
        except (TypeError, KeyError):
            raise ValueError("Repository data not found in response")

    def releases(self) -> dict[str, list]:
        """
        A JSON object with name of the repository, tag name, description and the created date and time.

        :returns: A dict object
        :rtype: dict
        """
        result = {"releases": []}
        after_cursor = None
        total = self._total_number_releases()

        while total > 0:
            after_query = f', after: "{after_cursor}"' if after_cursor else ""
            _json = {
                "query": f"""
                        query {{
                          repository(owner: \"{self.info.owner}\", name: \"{self.info.name}\") {{
                            releases(
                              first: 100
                              {after_query}
                              orderBy: {{field: CREATED_AT, direction: DESC}}
                            ) {{
                              pageInfo {{
                                hasNextPage
                                endCursor
                              }}
                              edges {{
                                node {{
                                  name
                                  tag {{
                                    name
                                  }}
                                  description
                                  createdAt
                                }}
                              }}
                            }}
                          }}
                        }}
                        """
            }

            r = requests.post(url=self.api_url, json=_json, headers=self.request_headers)

            try:
                response_data = r.json()
            except json.JSONDecodeError:
                raise requests.HTTPError(f"Invalid JSON response: {r.text}")

            new_releases = response_data["data"]["repository"]["releases"]["edges"]
            result["releases"].extend(new_releases)

            # Check if there are more pages
            page_info = response_data["data"]["repository"]["releases"]["pageInfo"]
            if page_info["hasNextPage"]:
                after_cursor = page_info["endCursor"]
                total -= 100  # Assuming each page returns 100 results
            else:
                break

        return result


class GitLabRequest(FormatBase):
    """
    GitLab request base.
    """

    def __init__(self, *args, **kwargs):
        super(GitLabRequest, self).__init__(*args, **kwargs)
        self.request_headers = {"Private-Token": "%s" % self.token}
        self.api_url = "https://gitlab.com/api/v4/"

        if self.token is None:
            raise InvalidToken(
                "Oops! GitLab requires you to generate a private token to get the details. See "
                "https://docs.gitlab.com/ce/user/profile/personal_access_tokens.html "
                "for more information."
            )

        if self.repo_url is not None:
            self.info = get_repo_url_info(self.location, repo_url=self.repo_url)
        else:
            self.info = get_repo_url_info(self.location)

    def _repo_id(self):
        """
        Searches and returns the repository ID based on the repository name. If the repository is not found then a table
        of repository is shown so that the user can manually enter the ID of their repository.

        :returns: Repository ID
        :return: id_number
        :rtype: int

        """
        url = self.api_url + f"projects?search={self.info.name}"

        r = requests.get(url=url, headers=self.request_headers)
        id_number = json.loads(r.text)

        if len(id_number) > 1:
            print(
                "The search resulted in more that one repository. Please check your repository name and type in it's ID"
            )
            print("ID - Repository Name - Username")

            for content in id_number:
                print(f"{content['id']} - {content['name']} - {multi_key_gitlab(content)}")

            id_number = input("ID > ")
            return id_number

        try:
            return id_number[0]["id"]
        except KeyError:
            raise KeyError("Wrong credentials given. Please check if you have the correct token.")

    def releases(self):
        """
        A JSON object containing name of the repository, tag name, description and the created date and time

        :returns: A dict object
        :rtype: dict
        """
        url = f"https://gitlab.com/api/v4/projects/{self._repo_id()}/repository/tags"

        r = requests.get(url=url, headers=self.request_headers)
        return json.loads(r.text)
