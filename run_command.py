import requests

def execute_command(command, minion_details):
    results = {}

    for minion, master_info in minion_details.items():

        for master, master_details in master_info.items():
        
            if master_info[master] != 'not found':
                url = master_details['url']
                auth_token = master_details['auth_token']
            

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
        

                

                response = requests.post(url, headers=headers, json=data, verify=False)
                
                if response.status_code == 200:
                    result_data = response.json()
                    results[minion] = {'master': master, 'result': result_data['return']}
                else:
                    results[minion] = {'master': master, 'error': f"HTTP Error {response.status_code}"}
            else: 
                results[minion] = {'master': 'not found', 'result': 'none'}
    return results






if __name__ == '__main__':
    minion_details = {'192.168.64.33': {'master1': {'url': 'https://192.168.64.30:8000', 'auth_token': '3f6611fb8c2777381a64f20ecd2647245a87c5c9'}}, 'myminion1': {'master1': {'url': 'https://192.168.64.30:8000', 'auth_token': '3f6611fb8c2777381a64f20ecd2647245a87c5c9'}}}
    command = 'test.ping'
    print(execute_command (command, minion_details))