
# import re
# import sys

import requests
# import getpass
import json

from .const import LOGGER

# Keyring stores passwords by a 'username', but we're not storing a username and
# password
import socket
fake_username = 'ipython_tools_%s' % socket.gethostname().replace('.',
                                                                  '_').replace('-', '_')


class Obj(dict):
    """Dictionary with attribute access to names."""

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError as e:
            raise AttributeError(name) from e

    def __setattr__(self, name, val):
        self[name] = val


token = None


class ChecklyApi:
    # def get_auth_token():
    #     global token
    #
    #     if token is not None:
    #         return token
    #
    #     import keyring
    #     token = keyring.get_password('github', fake_username)
    #     if token is not None:
    #         return token
    #
    #     print(
    #         "Get a token fom https://app.checklyhq.com/settings/api-tokens."
    #     )
    #     token = getpass.getpass("Token: ", stream=sys.stderr)
    #
    #     keyring.set_password('checkly', fake_username, token)
    #     return token

    def __init__(self, key, accountId):
        self._api_key = key
        self._checkly_account_id = accountId

    @property
    def _auth_header(self):
        return {
            'accept': 'application/json',
            'Authorization': 'Bearer ' + self._api_key,
            'x-checkly-account': self._checkly_account_id
        }

    @property
    async def get_checks(self):
        """Get all Checkly Checks."""
        url = 'https://api.checklyhq.com/v1/checks'
        headers = self._auth_header
        LOGGER.warn(f'RETURNED_HEADER {headers}')
        response = await requests.get(url, headers=headers)
        # response = await hass.async_add_executor_job(requests.get(url, headers=headers))
        LOGGER.warn(f'RESP.GET_CHECKS {response}')
        return response.json()

    @property
    def get_check_statuses(self):
        """Get all Checkly Checks."""
        url = 'https://api.checklyhq.com/v1/check-statuses'
        headers = self._auth_header
        response = requests.get(url, headers=headers)
        LOGGER.warn(f'RESP.GET_CHECK_STATUSES {response}')
        return response.json()

    # def get_pull_request(project, num, auth=False):
    #     """get pull request info  by number
    #     """
    #     url = "https://api.github.com/repos/{project}/pulls/{num}".format(
    #         project=project, num=num)
    #     if auth:
    #         header = make_auth_header()
    #     else:
    #         header = None
    #     print("fetching %s" % url, file=sys.stderr)
    #     response = requests.get(url, headers=header)
    #     response.raise_for_status()
    #     return json.loads(response.text, object_hook=Obj)
    #
    #
    # element_pat = re.compile(r'<(.+?)>')
    # rel_pat = re.compile(r'rel=[\'"](\w+)[\'"]')
    #
    #
    # def get_paged_request(url, headers=None, **params):
    #     """get a full list, handling APIv3's paging"""
    #     results = []
    #     params.setdefault("per_page", 100)
    #     while True:
    #         if '?' in url:
    #             params = None
    #             print("fetching %s" % url, file=sys.stderr)
    #         else:
    #             print("fetching %s with %s" % (url, params), file=sys.stderr)
    #         response = requests.get(url, headers=headers, params=params)
    #         response.raise_for_status()
    #         results.extend(response.json())
    #         if 'next' in response.links:
    #             url = response.links['next']['url']
    #         else:
    #             break
    #     return results
    #
    #
    # def get_issues_list(project, auth=False, **params):
    #     """get issues list"""
    #     params.setdefault("state", "closed")
    #     url = "https://api.github.com/repos/{project}/issues".format(
    #         project=project)
    #     if auth:
    #         headers = make_auth_header()
    #     else:
    #         headers = None
    #     pages = get_paged_request(url, headers=headers, **params)
    #     return pages
    #
    #
    # def get_milestones(project, auth=False, **params):
    #     params.setdefault('state', 'all')
    #     url = "https://api.github.com/repos/{project}/milestones".format(
    #         project=project)
    #     if auth:
    #         headers = make_auth_header()
    #     else:
    #         headers = None
    #     milestones = get_paged_request(url, headers=headers, **params)
    #     return milestones
    #
    #
    # def get_milestone_id(project, milestone, auth=False, **params):
    #     milestones = get_milestones(project, auth=auth, **params)
    #     for mstone in milestones:
    #         if mstone['title'] == milestone:
    #             return mstone['number']
    #     else:
    #         raise ValueError("milestone %s not found" % milestone)
    #
    #
    # def is_pull_request(issue):
    #     """Return True if the given issue is a pull request."""
    #     return bool(issue.get('pull_request', {}).get('html_url', None))
    #
    #
    # def get_authors(pr):
    #     print("getting authors for #%i" % pr['number'], file=sys.stderr)
    #     h = make_auth_header()
    #     r = requests.get(pr['commits_url'], headers=h)
    #     r.raise_for_status()
    #     commits = r.json()
    #     authors = []
    #     for commit in commits:
    #         author = commit['commit']['author']
    #         authors.append("%s <%s>" % (author['name'], author['email']))
    #     return authors
