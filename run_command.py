import requests 
from map_master import get_target_master

def run_command_on_minion(minion_id, command):

    target_master = get_target_master(minion_id)
    master_name = next(iter(target_master))
    url = target_master[master_name]['url']
    auth_token = target_master[master_name]['auth_token']

    if target_master == {'master': 'not found'}:
        print(f"No master details found for minion {minion_id}")
        return None

    headers = {
        'Accept': 'application/json',
        'X-Auth-Token': auth_token
    }
    data = {
        'client': 'local',
        'tgt': minion_id,
        'fun': 'cmd.run',
        'arg': command
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to execute command:", response.status_code, response.text)
        return None



if __name__ == '__main__':
    command_output = run_command_on_minion('myminion','test.ping')
    print(command_output)
