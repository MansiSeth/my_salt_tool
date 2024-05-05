import requests
from config import MASTER_URLS

def fetch_auth_tokens():
    auth_tokens = {}


    headers = {'Accept': 'application/json',
    'Content-Type': 'application/x-www-form-urlencoded'  
    }

    data = {
        'username': 'myuser',
        'password': '1234',
        'eauth': 'auto'
    }

    for master, base_url in MASTER_URLS.items():
        login_url = f"{base_url}/login"

        try:
            response = requests.post(login_url, headers=headers, data=data, verify=False)
            response.raise_for_status()  # Raises an HTTPError for bad responses
            auth_token = response.json().get('return', [{}])[0].get('token', 'No token retrieved')
            
            auth_tokens[master] = auth_token
        except requests.exceptions.RequestException as e:
            print(f"Failed to get auth token for {master}")
            auth_tokens[master] = 'Failed to get auth token'

    return auth_tokens

if __name__ == '__main__':
    tokens = fetch_auth_tokens()
    print(tokens)
