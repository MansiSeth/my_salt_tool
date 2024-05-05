import requests 
from auth_tokens import fetch_auth_tokens
from config import MASTER_URLS

def get_target_master(minion_id):

    target_master = {}

    master_urls = MASTER_URLS
    auth_tokens = fetch_auth_tokens()

    for master, url in master_urls.items():
        auth_token = auth_tokens[master]
        
        if auth_token != 'Failed to get auth token':
            # Define the headers and data payload for the request
            headers = {
                'Accept': 'application/json',
                'X-Auth-Token': auth_token
            }
            data = {
                'client': 'local',
                'tgt': minion_id,
                'fun': 'test.ping',
                'clear': True
            }
            
            # Perform the POST request
            response = requests.post(url, headers=headers, data=data, verify=False)
            
            # Check the response for a True result for the specified minion
            if response.ok:
                response_json = response.json()
                # Check if the response contains True for the target minion
                if response_json.get('return', [{}])[0].get(minion_id) == True:
                    print("successfully returning")
                    target_master[master] = {'url': url, 'auth_token': auth_token}
                    break

    if target_master == {}:
        target_master = {'master': 'not found'}

    return target_master 
        

if __name__ == '__main__':
    target_master = get_target_master('myminion2')
    print(target_master)


    