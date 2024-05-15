import os
import requests
import redis
from config import MASTER_URLS


# Setting up the Redis connection
auth_cache = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

def get_auth_token(master):

    #not handling the case of master not in config since this function is called from find master that passes 'master' as parameter by looping the config file

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded'  
    }

    data = {
        'username': 'myuser',
        'password': '1234',
        'eauth': 'auto'
    }

    # Fetching URL for that master from the config file
    login_url = f"{MASTER_URLS[master]}/login"

    # Check if the token is already in the cache
    auth_token = auth_cache.get(master)
    if auth_token:
        print('auth_token fetched from cache for ', master)
        return auth_token

    # Check if certificate for the master exists on the server
    cert_path = f'/etc/pki/tls/certs/{master}.crt'
    if not os.path.exists(cert_path):
        auth_token = 'Certificate not found'
    else:
        try:
            response = requests.post(login_url, headers=headers, data=data, verify=cert_path)
            auth_token = response.json().get('return', [{}])[0].get('token', 'No token retrieved') 


            # Store the token in Redis cache with expiration time of 10 minutes (600 seconds)
            if auth_token not in ('No token retrieved', 'Failed to get auth token'):
                auth_cache.setex(master, 60, auth_token)
        except requests.exceptions.RequestException:
            auth_token = 'Failed to get auth token'

    return auth_token

if __name__ == '__main__':
    tokens = get_auth_token('mymaster')
    print(tokens)

