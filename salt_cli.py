

import argparse 
# A module that lets us write CLI apps
from tabulate import tabulate
# A module to display data as a table on the CLI


from minionlist_map_master import map_masters_for_minionlist
from find_master import map_master
from run_command import execute_command
from target_type_detection import target_type_detection

def main():

    #Initializing the parser
    parser = argparse.ArgumentParser(
    prog = 'Proxy tool for multiple masters in Salt',
    description = 'Determine the correct master on which a given minion is configured and execute a given command'
    )

    #Defining options
    

    parser.add_argument("target", 
                        help="Specify the target of command",
                        type= str,
                        #required= True, 
                        #dest = 'target', #name of variable you want to call using args.__
    )

    parser.add_argument("command", 
                        help="Define the command to execute",
                        type= str,
                        #default = 'test.ping', 
                        #dest = 'command', #name of variable you want to call using args.__ 
    )

    #set default function to be executed 
    parser.set_defaults(func=run)

    #collect arguments passed by the user in CLI and store them in appropriate namespaces
    args = parser.parse_args()

    #passing arguments from CLI to func 'run'
    args.func(args)



def run(args) :

    target_type = target_type_detection(args.target)
    print('Your Target Type is: ', target_type)

    if target_type == 'glob':
        target_dict = map_master(args.target, 'glob')
        data = execute_command(args.command, target_dict) 

    elif target_type == 'list':
        minion_list = args.target.split(', ') #target is a string, needs to be split into comma separated list
        target_dict = map_masters_for_minionlist(minion_list)
        data = execute_command(args.command, target_dict)


    elif target_type == 'grain':
        target_dict = map_master(args.target, 'grain')
        data = execute_command(args.command, target_dict)

    elif target_type == 'regex':
        target_dict = map_master(args.target, 'pcre')
        data = execute_command(args.command, target_dict)
        
    
    elif target_type == 'ipcidr':
        target_dict = map_master(args.target, 'ipcidr')
        #target_dict2 = get_target_master(args.target)
        #print(target_dict)
        #print(target_dict2)
        data = execute_command(args.command, target_dict)

    elif target_type == 'nodegroup':
        target_dict = map_master(args.target, 'nodegroup')
        data = execute_command(args.command, target_dict)

    elif target_type == 'compound':
        target_dict = map_master(args.target, 'compound')
        data = execute_command(args.command, target_dict)



    #Using tabulate to format the result dictionary 'data'
    """ 
    data = {
        '192.168.64.32': {
            'master': 'master1',
            'result': [{'myminion': True}]
        },
        'myminion1': {
            'master': 'master1',
            'result': [{'myminion1': True}]
        }
    }
    """
    
    table_data = []
    for minion, details in data.items():
        master = details['master']
        result_payload = details['result']
        table_data.append((minion, master, result_payload))
    
    table = tabulate(table_data, headers=['Minion', 'Master', 'Result Payload'], tablefmt='fancy_grid')
    print(table)

#Defining entrypoint of CLI app
# this ensures that script is run only from the CLI not when it's imported into another script
#__name__ is a built in variable in python 
#value of __name__ is '__main__' if its called in the script that's running 
#value of __name__ is the name of file being imported to another (here, argparse_cheatsheet) if module is imported

if __name__=="__main__":
    main()