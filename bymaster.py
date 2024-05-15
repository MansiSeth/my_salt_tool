import requests
from get_auth_token import get_auth_token
from config import MASTER_URLS


def bymaster(command, master):
    results = {}
    


    if master in MASTER_URLS:
        url = MASTER_URLS[master]  # Retrieve URL for the master
        
        auth_token = get_auth_token(master)
        
        cert_path = f'/etc/pki/tls/certs/{master}.crt'


        if auth_token in ('Failed to get auth token', 'Certificate not found'):
            return {'no minion': {'master': master, 'result': 'Failed to authenticate or certificate missing'}}
        
        
        else: 
            headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'X-Auth-Token': auth_token
            }

            data = {
                "client": "local",
                "tgt": '*',
                "fun": command.split()[0],
            }

            #if command has an argument only then its passed with 'arg' key
            if len(command.split()) > 1:
                data['arg'] = command.split()[1]

            response = requests.post(url, headers=headers, json=data, verify= cert_path)
                    
            if response.status_code == 200:
                result_data = response.json()


                for minion, payload in result_data.get('return', [{}])[0].items():
                        results[minion] = {'master': master, 'result': payload}
                        # even though all minions will have same master value, 
                        #returning master so that it can be uniformly displayed in the salt_cli.py's tabulate table 

            else: 
                results = {'no minion': {'master': master, 'result': 'Could not connect to master'}}

                
        return results
    
    else: 
        return {'no minion': {'master': master, 'result': 'Master URL not found in configuration'}}


    



if __name__ == '__main__':
    master = 'mymaster1'
    command = 'test.ping'
    print(bymaster(command, master))