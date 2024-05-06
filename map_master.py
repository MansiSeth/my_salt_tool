import requests 
from auth_tokens import fetch_auth_tokens
from config import MASTER_URLS

def get_target_master(minion):

    target_master = {}

    if '.' in minion:
        target_type = 'ipcidr'
    else:
        target_type = 'glob'

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
                'tgt': minion,
                'fun': 'test.ping',
                'clear': True,
                'tgt_type': target_type
            }
            
            # Perform the POST request
            response = requests.post(url, headers=headers, data=data, verify=False)
            
            
            if response.ok: #status code in 200s
                response_json = response.json()

                """
                We need to dynamically check if value for 1st key is true 
                We cant reference by minion since it could be an ip 
                response_json.get('return', [{}])[0].get(minion) == True: 
                """

                first_return_item = response_json.get('return', [{}])[0] 
                # Response will be of the type {"return": [{"myminion": true}]} so first return item is {"myminion": true}
                
                if next(iter(first_return_item.values()), None) == True:  #key value of first (and only) dictionary is true
                    target_master =  {next(iter(first_return_item)):{master: {'url': url, 'auth_token': auth_token}}}
                    break

    if target_master == {}:
        target_master = {minion: {'master': 'not found'}}

    return target_master 
        

if __name__ == '__main__':
    target_master = get_target_master('my')
    print(target_master)


    