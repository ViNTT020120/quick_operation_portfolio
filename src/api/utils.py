import requests
import json

class APIClient:
    def __init__(self, base_url, client_id, client_secret):
        self.base_url = base_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = None

    def log_in(self, username, password):
        param = {
            'grant_type': 'password',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'username': username,
            'password': password
        }
        url = f"{self.base_url}/login"
        resp = requests.post(url, data=param)
        outcome = json.loads(resp.text)
        self.token = outcome['accessToken']
        return self.token

    def get_headers(self):
        if not self.token:
            raise ValueError("Token is not available. Please log in first.")
        return {'Authorization': f'jwt {self.token}'}

    def get(self, path, params=None):
        url = f"{self.base_url}{path}"
        headers = self.get_headers()
        resp = requests.get(url, params=params, headers=headers)
        return json.loads(resp.text)