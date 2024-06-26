import requests

from minionlist_find_master import minionlist_find_master
#Testing use
#not used unless calling script from terminal, miniondetails gets passed as a param from cli app where this is called already 
 

def run_command(command, minion_details):
    results = {}

    for minion, master_info in minion_details.items():

        for master, master_details in master_info.items():

        
            if master_info[master] != 'not found':
                url = master_details['url']
                auth_token = master_details['auth_token']
                cert_path = f'/etc/pki/tls/certs/{master}.crt'
            

                headers = {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    'X-Auth-Token': auth_token
                }



                data = {
                    "client": "local",
                    "tgt": minion,
                    "fun": command.split()[0],
                }

                #if command has an argument only then its passed with 'arg' key
                if len(command.split()) > 1:
                    data['arg'] = command.split()[1]

                #if minion was passed by ip and target dictionary contains key as ip 
                if '.' in minion:
                    data['tgt_type'] = 'ipcidr'
        

                

                response = requests.post(url, headers=headers, json=data, verify= cert_path)
                
                if response.status_code == 200:
                    result_data = response.json()
                    results[minion] = {'master': master, 'result': result_data['return']}
                else:
                    results[minion] = {'master': master, 'error': f"HTTP Error {response.status_code}"}
            else: 
                results[minion] = {'master': 'not found', 'result': 'none'}
    return results





if __name__ == '__main__':
    minion_details = minionlist_find_master(['192.168.64.34','myminion1'])
    command = 'test.ping'
    print(run_command(command, minion_details))