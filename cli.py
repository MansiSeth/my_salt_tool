import argparse 
# A module that lets us write CLI apps

from map_master import get_target_master
from minionlist_map_master import map_masters_for_minionlist
from complex_map_master import complex_target_map_master

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
                        choices = ['minion_id','minion_list', 'grain', 'regex', 'ip']
    )

    parser.add_argument("--tgt", 
                        help="Specify the target of command",
                        type= str,
                        required= True,
                        default = 'myminion1', 
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
        print(target_dict)

    elif args.target_type == 'minion_list':
        target_dict = map_masters_for_minionlist(args.target)
        print(target_dict)

    elif args.target_type == 'grain':
        target_dict = complex_target_map_master(args.target, 'grain')
        print(target_dict)

    elif args.target_type == 'regex':
        target_dict = complex_target_map_master(args.target, 'glob')
        print(target_dict)
    
    elif args.target_type == 'ip':
        target_dict = complex_target_map_master(args.target, 'ipcidr')
        print(target_dict)

    

#Defining entrypoint of CLI app
# this ensures that script is run only from the CLI not when it's imported into another script
#__name__ is a built in variable in python 
#value of __name__ is '__main__' if its called in the script that's running 
#value of __name__ is the name of file being imported to another (here, argparse_cheatsheet) if module is imported

if __name__=="__main__":
    main()