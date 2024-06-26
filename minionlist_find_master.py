from find_master import find_master
from target_type_detection import target_type_detection

def minionlist_find_master(minionlist):
    minionlist_master_map = {}

    for minion in minionlist: #minion is what's passed, maybe an ip
        #master_info = get_target_master(minion) #gives single item dictionary whose key is minion_id of ip/minion passed and value is a nested dictionary with master details
        
        target_type = target_type_detection(minion)


        master_info = find_master(minion, target_type)
        
        for minion_id, master_dict in master_info.items():

            minionlist_master_map[minion] = master_info[minion_id] 
            #making a multi-item dictionary whose key is what's passed (ip/id) and value is master detail dict
        
        
    return minionlist_master_map

if __name__ == '__main__':
    minionlist = ['myminion1','192.168.64.55']
    master_mapping = minionlist_find_master(minionlist)
    print(master_mapping)