import requests
from config import MASTER_URLS
from auth_tokens import fetch_auth_tokens

# Supports glob,grains, regex, IP address (ipcidr), compound
# sends test.ping to all masters with their respective auth tokens if token is found using auth_tokens module
# Whichever master returned true in their response is mapped to the minion key in the dictionary 
# returns a dictionary of the form {minion: master : {url: __, auth_token:__}}

def complex_target_map_master(complex_target, target_type):
    master_urls = MASTER_URLS
    auth_tokens = fetch_auth_tokens()

    result_minions = {}

    for master, url in master_urls.items():
        auth_token = auth_tokens[master]
        cert_path = f'/etc/pki/tls/certs/{master}.crt'

    
    
        
        if auth_token not in ('Failed to get auth token', 'Certificate not found'):
            headers = {
                'Accept': 'application/json',
                'X-Auth-Token': auth_token  # Use the auth token for each master
            }
            
            payload = {
                'client': 'local',
                'tgt': complex_target,
                'tgt_type': target_type,
                'fun': 'test.ping'
            }


            response = requests.post(url, headers=headers, json=payload, verify=cert_path)
           
            
            if response.status_code == 200:
                try:
                    data = response.json()

                    """
                    return payload is a dictionary with return as a key and a list as the value 
                    the list contains a dictionary with key minion_id
                    {'return': [{'myminion5': True, 'myminion2': True}]}
                    Hence accessing the list with data['return'][0]
                    """

                    for minion, status in data['return'][0].items(): 
                        if status:  # If the minion responded with True
                            if minion not in result_minions:
                                result_minions[minion] = {}
                            result_minions[minion][master] = {'url': url, 'auth_token': auth_token}
                except ValueError:
                    print(f"Failed to decode JSON from response of {master}")
        
            if result_minions == {}:
                result_minions = {minion: {'master': 'not found'}}

    return result_minions  



if __name__ == '__main__':
    complex_target = "group1"
    target_type = 'nodegroup'
    minions = complex_target_map_master(complex_target, target_type)
    print(minions)
