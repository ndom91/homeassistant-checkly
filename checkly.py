import requests

from .const import API_BASE_URL


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

    def _get_auth_header(self):
        return {
            'accept': 'application/json',
            'Authorization': 'Bearer ' + self._api_key,
            'x-checkly-account': self._checkly_account_id
        }

    def get_checks(self):
        """Get all Checkly Checks."""
        url = f'{API_BASE_URL}/checks'
        headers = self._get_auth_header()
        response = requests.get(url, headers=headers)
        return response.json()

    def get_check_statuses(self):
        """Get all Checkly Checks."""
        url = f'{API_BASE_URL}/check-statuses'
        headers = self._get_auth_header()
        response = requests.get(url, headers=headers)
        return response.json()
