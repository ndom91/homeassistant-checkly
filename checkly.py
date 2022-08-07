import requests

from .const import LOGGER


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


class ChecklyApi():
    def __init__(self, key, accountId):
        self._api_key = key
        self._checkly_account_id = accountId

    def _auth_header(self):
        return {
            'accept': 'application/json',
            'Authorization': 'Bearer ' + self._api_key,
            'x-checkly-account': self._checkly_account_id
        }

    def get_checks(self):
        """Get all Checkly Checks."""
        url = 'https://api.checklyhq.com/v1/checks'
        headers = self._auth_header()
        response = requests.get(url, headers=headers)
        LOGGER.warn(f'RESP.GET_CHECKS {response}')
        body = response.json()
        return body

    def get_check_statuses(self):
        """Get all Checkly Checks."""
        url = 'https://api.checklyhq.com/v1/check-statuses'
        headers = self._auth_header()
        response = requests.get(url, headers=headers)
        LOGGER.warn(f'RESP.GET_CHECK_STATUSES {response}')
        body = response.json()
        return body
