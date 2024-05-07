

import argparse 
# A module that lets us write CLI apps
from tabulate import tabulate
# A module to display data as a table on the CLI


from map_master import get_target_master
from minionlist_map_master import map_masters_for_minionlist
from complex_map_master import complex_target_map_master
from run_command import execute_command

def main():

    #Initializing the parser
    parser = argparse.ArgumentParser(
    prog = 'Proxy tool for multiple masters in Salt',
    description = 'Determine the correct master on which a given minion is configured and execute a given command'
    )

    #Defining options
    parser.add_argument("--typ", 
                        help="Specify the type of targetting used",
                        type= str,
                        required= True,
                        default = 'minion_id', 
                        dest ='target_type', #name of variable you want to call using args.__ 
                        choices = ['minion_id','minion_list', 'minionip_list', 'grain', 'regex', 'ip']
    )

    parser.add_argument("--tgt", 
                        help="Specify the target of command",
                        type= str,
                        required= True, 
                        dest = 'target', #name of variable you want to call using args.__
    )

    parser.add_argument("--c", 
                        help="Define the command to execute",
                        type= str,
                        default = 'test.ping', 
                        dest = 'command', #name of variable you want to call using args.__ 
    )

    #set default function to be executed 
    parser.set_defaults(func=run)

    #collect arguments passed by the user in CLI and store them in appropriate namespaces
    args = parser.parse_args()

    #passing arguments from CLI to func 'run'
    args.func(args)



def run(args) :

    if args.target_type == 'minion_id':
        target_dict = get_target_master(args.target)
        data = execute_command(args.command, target_dict)

    elif args.target_type == 'minion_list':
        minion_list = args.target.split(', ')
        target_dict = map_masters_for_minionlist(minion_list)
        data = execute_command(args.command, target_dict)


    elif args.target_type == 'grain':
        target_dict = complex_target_map_master(args.target, 'grain')
        data = execute_command(args.command, target_dict)

    elif args.target_type == 'regex':
        target_dict = complex_target_map_master(args.target, 'glob')
        data = execute_command(args.command, target_dict)
        
    
    elif args.target_type == 'ip':
        target_dict = complex_target_map_master(args.target, 'ipcidr')
        data = execute_command(args.command, target_dict)

    table_data = []
    for minion, details in data.items():
        master = details['master']
        result_payload = details['result']
        table_data.append((minion, master, result_payload))
    
    table = tabulate(table_data, headers=['Minion', 'Master', 'Result Payload'], tablefmt='pipe')
    print(table)

#Defining entrypoint of CLI app
# this ensures that script is run only from the CLI not when it's imported into another script
#__name__ is a built in variable in python 
#value of __name__ is '__main__' if its called in the script that's running 
#value of __name__ is the name of file being imported to another (here, argparse_cheatsheet) if module is imported

if __name__=="__main__":
    main()