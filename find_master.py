import requests
import redis
from config import MASTER_URLS

from new_auth_token import fetch_auth_token_for_master

# Supports grains, regex, IP address (ipcidr)
# sends test.ping to all masters with their respective auth tokens if token is found using auth_tokens module
# Whichever master returned true in their response is mapped to the minion key in the dictionary 
# returns a dictionary of the form {minion: master : {url: __, auth_token:__}}


target_cache = redis.Redis(host='localhost', port=6379, db=1, decode_responses=True)

def map_master(target, target_type):
    master_urls = MASTER_URLS

    result_minions = {}



    cache_info = target_cache.hgetall(target)
    
    # Target maybe a grain which is satisfied by multiple minions on multiple masters
    # cache_info is of the form {'myminion3': 'mymaster1', 'myminion2': 'mymaster2'...} 
    # for minion_id and ip target type it's single item dictionary {'myminion3': 'mymaster1'}
    
    if cache_info:

        print(target , ' Found In Cache')

        for minion, master in cache_info.items():

            if master in master_urls:
                url = master_urls[master]  # Retrieve URL for the master
                auth_token = fetch_auth_token_for_master(master)  # Fetch the auth token for the master

                # Check if the auth token retrieval was successful
                if auth_token not in ('Failed to get auth token', 'Certificate not found'):
                    result_minions[minion] = {
                        master: {
                            'url': url,
                            'auth_token': auth_token
                        }
                    }
                else:
                    print(f"Failed to fetch auth token for {master}")

        return result_minions  
    



    
    if not cache_info:
        for master, url in master_urls.items():

            auth_token = fetch_auth_token_for_master(master)

            cert_path = f'/etc/pki/tls/certs/{master}.crt'

        
            
            if auth_token not in ('Failed to get auth token', 'Certificate not found'):
                headers = {
                    'Accept': 'application/json',
                    'X-Auth-Token': auth_token  # Use the auth token for each master
                }
                
                payload = {
                    'client': 'local',
                    'tgt': target,
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
                                

                                result_minions[minion] = {
                                    master: {
                                        'url': url,
                                        'auth_token': auth_token
                                    }
                                }
                                target_cache.hset(target, minion, master)

        

                    except ValueError:
                        print(f"Failed to decode JSON from response of {master}")
            
                else:
                    print(f"Failed to reach {master}, status code {response.status_code}")

        if result_minions == {}:
            result_minions[target] = {'master': 'not found'}


        return result_minions  



if __name__ == '__main__':

    target = "mycolor:red"
    target_type = 'grain'
    minions = map_master(target, target_type)
    print(minions)
